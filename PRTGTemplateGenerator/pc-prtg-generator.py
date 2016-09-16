#!/usr/bin/env python
from urllib2 import Request, urlopen, URLError
import sys
import argparse
from urlparse import urlparse
import re
import xml.etree.ElementTree as ET
import uuid
import csv

# Constants
PRINTER_SERVER_COLUMN = 0
PRINTER_NAME_COLUMN = 1
PRINTER_LOCATION_COLUMN = 2
PRINTER_URL_COLUMN = 3

DEVICE_NAME_COLUMN = 0
DEVICE_LOCATION_COLUMN = 1
DEVICE_URL_COLUMN = 2

# Enums

class CheckType:
    PING = 1
    DOTNET = 2


class SensorType:
    HTTP = 1
    XML = 2


class DeviceType:
    PRINTER = 1
    DEVICE = 2


# XML Utils
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def writeXMLFile(root, **kwargs):
    filename = kwargs.get('filename', str(uuid.uuid4()) + '.odt')

    indent(root)
    document = ET.ElementTree(root)
    document.write(filename, encoding='utf-8', xml_declaration=True)
    print 'Template saved: {0}'.format(filename)


# PRTG Node Generation
def createCheckNode(checkType):
    if checkType is CheckType.PING:
        node = ET.Element('check')
        node.set('id', 'ping')
        node.set('meta', 'ping')
        return node
    elif checkType is CheckType.DOTNET:
        node = ET.Element('check')
        node.set('id', 'dotnet40')
        node.set('meta', 'dotnet')
        node.set('requires', 'ping')

        metadata = ET.SubElement(node, 'metadata')
        requireddotnetversion = ET.SubElement(
            metadata, 'requireddotnetversion')
        requireddotnetversion.text = '40'
        return node
    else:
        raise TypeError


def createSensorNode(sensorType, displayName, tags, url, **kwargs):
    xmlNode = kwargs.get('xml_node', '')

    node = ET.Element('create')
    node.set('id', str(uuid.uuid4()))
    node.set('displayname', displayName)

    createData = ET.SubElement(node, 'createdata')

    ET.SubElement(createData, 'tags').text = tags
    ET.SubElement(createData, 'priority').text = '3'

    if sensorType == SensorType.HTTP:
        node.set('requires', 'ping')
        node.set('kind', 'http')
        ET.SubElement(createData, 'httpurl').text = url
    elif sensorType == SensorType.XML:
        node.set('requires', 'dotnet40')
        node.set('kind', 'ptfhttpxmlrestvalue')
        ET.SubElement(createData, 'xmlurl').text = url
        ET.SubElement(createData, 'xmlnode').text = xmlNode
    else:
        return None

    return node


def createDeviceTemplateRoot(**kwargs):
    root = ET.Element('devicetemplate')
    root.set('id', kwargs.get('id', ''))
    root.set('name', kwargs.get('name', ''))
    root.set('priority', kwargs.get('priority', '40'))
    root.set('adddevicename', kwargs.get('name', ''))

    return root


def buildServerTemplate(server):
    print 'Creating PRTG PaperCut Server Template...'
    root = createDeviceTemplateRoot(id='pc-server',
                                    name='PaperCut Server')

    root.append(createCheckNode(CheckType.PING))
    root.append(createCheckNode(CheckType.DOTNET))

    root.append(createSensorNode(SensorType.HTTP,
                                 'Overall Server Health',
                                 'server',
                                 server.getServerHealthNodeUrl()))

    root.append(createSensorNode(SensorType.XML,
                                 'Held Jobs',
                                 'held_jobs',
                                 server.getHeldJobsNodeUrl(),
                                 xml_node='heldJobsCount'))

    root.append(createSensorNode(SensorType.XML,
                                 'Recent Pages Printed (1m)',
                                 'pages_printed',
                                 server.getRecentPagesNodeUrl(),
                                 xml_node='recentPagesCount'))

    root.append(createSensorNode(SensorType.XML,
                                 'Recent Errors (10m)',
                                 'recent_errors',
                                 server.getRecentErrorsNodeUrl(),
                                 xml_node='recentErrorsCount'))

    root.append(createSensorNode(SensorType.XML,
                                 'Recent Warnings (10m)',
                                 'recent_warnings',
                                 server.getRecentWarningsNodeUrl(),
                                 xml_node='recentWarningsCount'))

    return root


def buildPrinterTemplate(printerCollection):
    print 'Creating PRTG Printer Template...'
    root = createDeviceTemplateRoot(id='pc-printers',
                                    name='PaperCut Printers')

    root.append(createCheckNode(CheckType.PING))
    for printer in printerCollection:
        root.append(printer.createXMLNode())

    return root


def buildDeviceTemplate(deviceCollection):
    print 'Creating PRTG Device Template...'
    root = createDeviceTemplateRoot(id='pc-devices',
                                    name='PaperCut Devices')

    root.append(createCheckNode(CheckType.PING))
    for device in deviceCollection:
        root.append(device.createXMLNode())

    return root


# Filter Generator
def filterCSV(csvReader, server, location, deviceType):
    for row in csvReader:
        if filterByServer(row, server, deviceType) and filterByLocation(row, location, deviceType):
            yield row


def filterByServer(row, server, deviceType):
    if server is None:
        return True
    if deviceType is DeviceType.DEVICE:
        return True
    return row[PRINTER_SERVER_COLUMN] == server


def filterByLocation(row, location, deviceType):
    if location is None:
        return True
    if deviceType is DeviceType.DEVICE:
        return row[DEVICE_LOCATION_COLUMN] == location
    if deviceType is DeviceType.PRINTER:
        return row[PRINTER_LOCATION_COLUMN] == location


# Build Device Data
def createPrinterCollection(source, max):
    currentCount = 0
    printerCollection = []
    for row in source:
        printerCollection.append(Printer(printer_server=row[PRINTER_SERVER_COLUMN],
                                         printer_name=row[PRINTER_NAME_COLUMN],
                                         printer_location=row[PRINTER_LOCATION_COLUMN],
                                         status_url=row[PRINTER_URL_COLUMN],
                                         device_type=DeviceType.PRINTER))
        currentCount += 1
        if currentCount >= max:
            break
    return printerCollection


def createDeviceCollection(source, max):
    currentCount = 0
    deviceCollection = []
    for row in source:
        deviceCollection.append(Printer(printer_name=row[DEVICE_NAME_COLUMN],
                                        printer_location=row[DEVICE_LOCATION_COLUMN],
                                        status_url=row[DEVICE_URL_COLUMN],
                                        device_type=DeviceType.DEVICE))
        currentCount += 1
        if currentCount >= max:
            break
    return deviceCollection


class PapercutServer:

    def __init__(self, address, authkey, port):
        self.address = address
        self.authkey = authkey
        self.port = port

    # API Urls
    def getServerHealthNodeUrl(self):
        return 'http://{0}:{2}/api/health?Authorization={1}'.format(self.address, self.authkey, self.port)

    def getHeldJobsNodeUrl(self):
        return 'http://{0}:{2}/api/stats/held-jobs-count?Authorization={1}'.format(self.address, self.authkey, self.port)

    def getRecentPagesNodeUrl(self):
        return 'http://{0}:{2}/api/stats/recent-pages-count?minutes=1&Authorization={1}'.format(self.address, self.authkey, self.port)

    def getRecentErrorsNodeUrl(self):
        return 'http://{0}:{2}/api/stats/recent-errors-count?minutes=10&Authorization={1}'.format(self.address, self.authkey, self.port)

    def getRecentWarningsNodeUrl(self):
        return 'http://{0}:{2}/api/stats/recent-warnings-count?minutes=1&Authorization={1}'.format(self.address, self.authkey, self.port)

    # CSV Urls
    def getPrintersCSVUrl(self):
        return 'http://{0}:{2}/api/health/printers/urls?Authorization={1}'.format(self.address, self.authkey, self.port)

    def getDevicesCSVUrl(self):
        return 'http://{0}:{2}/api/health/devices/urls?Authorization={1}'.format(self.address, self.authkey, self.port)


class Printer:

    def __init__(self, **kwargs):
        self.printerServer = kwargs.get('printer_server', None)
        self.printerName = kwargs.get('printer_name', None)
        self.printerLocation = kwargs.get('printer_location', None)
        self.statusUrl = kwargs.get('status_url', None)
        self.deviceType = kwargs.get('device_type', None)

    def createXMLNode(self):
        if self.deviceType is DeviceType.PRINTER:
            displayName = '{0}/{1}'.format(self.printerServer,
                                           self.printerName)
            tags = 'printer'
        elif self.deviceType is DeviceType.DEVICE:
            displayName = '{0}'.format(self.printerName)
            tags = 'device'
        else:
            raise TypeError

        return createSensorNode(SensorType.HTTP,
                                displayName,
                                tags,
                                self.statusUrl)


def main():
    address = o.hostname
    port = '80'
    if o.port is not None:
        port = o.port
    authkey = re.split('[=&]+', o.query)[-1]

    server = PapercutServer(address, authkey, port)
    print 'Connecting to PaperCut Installation at {0}:{1}'.format(server.address, server.port)
    print 'Filtering:\n\tserver:\t\t{0}\n\tlocation:\t{1}'.format(args.server, args.location)

    # Printers
    printerRequest = Request(server.getPrintersCSVUrl())
    try:
        printerResponse = urlopen(printerRequest)
    except URLError, e:
        print e
        return e

    printerList = csv.reader(printerResponse)
    printerList.next()

    print 'Reading Printer URLs...'
    printerCollection = createPrinterCollection(filterCSV(
        printerList, args.server, args.location, DeviceType.PRINTER), args.limit)

    if len(printerCollection) is 0:
        print 'No printers found.'
    else:
        printerTemplate = buildPrinterTemplate(printerCollection)
        writeXMLFile(printerTemplate, filename='PaperCut Printers.odt')

    # Devices
    deviceRequest = Request(server.getDevicesCSVUrl())
    try:
        deviceResponse = urlopen(deviceRequest)
    except URLError, e:
        print e
        return e

    deviceList = csv.reader(deviceResponse)
    deviceList.next()

    print 'Reading Device URLs...'
    deviceCollection = createDeviceCollection(filterCSV(
        deviceList, args.server, args.location, DeviceType.DEVICE), args.limit)

    if len(deviceCollection) is 0:
        print 'No devices found.'
    else:
        deviceTemplate = buildDeviceTemplate(deviceCollection)
        writeXMLFile(deviceTemplate, filename='PaperCut Devices.odt')

    # Server
    serverTemplate = buildServerTemplate(server)
    writeXMLFile(serverTemplate, filename='PaperCut Server.odt')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate PaperCut Printer and Device status templates for PRTG')
    parser.add_argument('address',
                        help='The GET query URL for your PaperCut Server Health API'+
                            ' (See Options->Advanced->System Health Monitoring)'+
                            ' example: http://203.0.113.0:9191/api/health/?Authorization=authKey1234')

    parser.add_argument('-lo', '--location', default=None,
                        help='Filter by location (default none)')

    parser.add_argument('-s', '--server', default=None,
                        help='Filter by server (default none)')

    parser.add_argument('-li', '--limit', default=250, type=int,
                        help='Maximum number of printers to include in template (default 250)')

    args = parser.parse_args()
    o = urlparse(args.address)
    main()
