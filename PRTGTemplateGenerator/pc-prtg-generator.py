#!/usr/bin/env python3
import sys
import argparse
import re
import xml.etree.ElementTree as ET
from csv import reader
from urllib.request import Request, urlopen, URLError
from urllib.parse import urlparse
from itertools import islice
from codecs import iterdecode
from uuid import uuid4

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
    filename = kwargs.get('filename', str(uuid4()) + '.odt')

    indent(root)
    document = ET.ElementTree(root)
    document.write(filename, encoding='utf-8', xml_declaration=True)
    print('Template saved: {0}'.format(filename))

# PRTG Primitive Nodes
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
    node.set('id', str(uuid4()))
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

# PRTG Composite Nodes
def buildServerTemplate(server):
    print('Creating PRTG PaperCut Server Template...')
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


def buildPrinterTemplate(printerCollection, **kwargs):
    id = kwargs.get('id', '')
    name = kwargs.get('name', '')
    root = createDeviceTemplateRoot(id=id,
                                    name=name)

    root.append(createCheckNode(CheckType.PING))
    for printer in printerCollection:
        root.append(printer.createXMLNode())

    return root

# Filters
def filterCSV(csvReader, predicateList):
    for row in csvReader:
        if all(f(row) for f in predicateList):
            yield row


def namePredicate(name):
    return lambda row: name in row[PRINTER_NAME_COLUMN]


def serverPredicate(server, deviceType):
    if deviceType is DeviceType.DEVICE:
        return lambda row: True
    if deviceType is DeviceType.PRINTER:
        return lambda row: server in row[PRINTER_SERVER_COLUMN]
    return TypeError


def locationPredicate(location, deviceType):
    if deviceType is DeviceType.DEVICE:
        return lambda row: location in row[DEVICE_LOCATION_COLUMN]
    if deviceType is DeviceType.PRINTER:
        return lambda row: location in row[PRINTER_LOCATION_COLUMN]
    return TypeError


def consolidatePredicates(args, deviceType):
    predicateList = []
    if args.server is not None:
        predicateList.append(serverPredicate(str(args.server), deviceType))
    if args.location is not None:
        predicateList.append(locationPredicate(str(args.location), deviceType))
    if args.name is not None:
        predicateList.append(namePredicate(str(args.name)))

    return predicateList

# Build Printer Data
def createPrinterCollection(source, max):
    printerCollection = []
    for row in islice(source, max):
        printerCollection.append(Printer(row[PRINTER_NAME_COLUMN],
                                         row[PRINTER_LOCATION_COLUMN],
                                         row[PRINTER_URL_COLUMN],
                                         DeviceType.PRINTER,
                                         printer_server=row[PRINTER_SERVER_COLUMN]))
    return printerCollection


def createDeviceCollection(source, max):
    deviceCollection = []
    for row in islice(source, max):
        deviceCollection.append(Printer(row[DEVICE_NAME_COLUMN],
                                        row[DEVICE_LOCATION_COLUMN],
                                        row[DEVICE_URL_COLUMN],
                                        DeviceType.DEVICE))
    return deviceCollection


class PapercutServer:

    def __init__(self, address, authkey, port):
        self.address = address
        self.authkey = authkey
        self.port = port

    # API Urls
    def getServerHealthNodeUrl(self):
        return 'http://{0}:{2}/api/health?Authorization={1}'\
            .format(self.address, self.authkey, self.port)

    def getHeldJobsNodeUrl(self):
        return 'http://{0}:{2}/api/stats/held-jobs-count?Authorization={1}'\
            .format(self.address, self.authkey, self.port)

    def getRecentPagesNodeUrl(self):
        return 'http://{0}:{2}/api/stats/recent-pages-count?minutes=1&Authorization={1}'\
            .format(self.address, self.authkey, self.port)

    def getRecentErrorsNodeUrl(self):
        return 'http://{0}:{2}/api/stats/recent-errors-count?minutes=10&Authorization={1}'\
            .format(self.address, self.authkey, self.port)

    def getRecentWarningsNodeUrl(self):
        return 'http://{0}:{2}/api/stats/recent-warnings-count?minutes=1&Authorization={1}'\
            .format(self.address, self.authkey, self.port)

    # CSV Urls
    def getPrintersCSVUrl(self):
        return 'http://{0}:{2}/api/health/printers/urls?Authorization={1}'\
            .format(self.address, self.authkey, self.port)

    def getDevicesCSVUrl(self):
        return 'http://{0}:{2}/api/health/devices/urls?Authorization={1}'\
            .format(self.address, self.authkey, self.port)


class Printer:

    def __init__(self, printerName, printerLocation, statusUrl, deviceType, **kwargs):
        self.printerServer = kwargs.get('printer_server', '')
        self.printerName = printerName
        self.printerLocation = printerLocation
        self.statusUrl = statusUrl
        self.deviceType = deviceType

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
    address = pcUrl.hostname
    port = '80'
    if pcUrl.port is not None:
        port = pcUrl.port
    authkey = re.split('[=&]', pcUrl.query)[-1]

    server = PapercutServer(address, authkey, port)
    print('Connecting to PaperCut Installation at {0}:{1}'
          .format(server.address, server.port))
    print('Filtering:\n\tServer:\t\t{0}\n\tLocation:\t{1}\n\tName:\t\t{2}'
          .format(args.server, args.location, args.name))

    # Printers
    printerRequest = Request(server.getPrintersCSVUrl())
    try:
        printerResponse = urlopen(printerRequest)
    except URLError as e:
        print(e)
        return e

    printerList = reader(iterdecode(printerResponse, 'utf-8'))
    next(printerList, None)

    print('Reading Printer URLs...')
    printerPredicateList = consolidatePredicates(args, DeviceType.PRINTER)
    if len(printerPredicateList) is not 0:
        printerCollection = createPrinterCollection(
            filterCSV(printerList, printerPredicateList), args.limit)
    else:
        printerCollection = createPrinterCollection(printerList, args.limit)

    if len(printerCollection) is 0:
        print('No printers found.')
    else:
        printerTemplate = buildPrinterTemplate(printerCollection,
                                               id='pc-printers',
                                               name='PaperCut Printers')
        writeXMLFile(printerTemplate, filename='PaperCut Printers.odt')

    # Devices
    deviceRequest = Request(server.getDevicesCSVUrl())
    try:
        deviceResponse = urlopen(deviceRequest)
    except URLError as e:
        print(e)
        return e

    deviceList = reader(iterdecode(deviceResponse, 'utf-8'))
    next(deviceList, None)

    print('Reading Device URLs...')
    devicePredicateList = consolidatePredicates(args, DeviceType.DEVICE)
    if len(devicePredicateList) is not 0:
        deviceCollection = createDeviceCollection(
            filterCSV(deviceList, devicePredicateList), args.limit)
    else:
        deviceCollection = createDeviceCollection(deviceList, args.limit)

    if len(deviceCollection) is 0:
        print('No devices found.')
    else:
        deviceTemplate = buildPrinterTemplate(deviceCollection,
                                              id='pc-devices',
                                              name='PaperCut Printers')
        writeXMLFile(deviceTemplate, filename='PaperCut Devices.odt')

    # Server
    serverTemplate = buildServerTemplate(server)
    writeXMLFile(serverTemplate, filename='PaperCut Server.odt')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate PaperCut Printer and Device status templates for PRTG')
    parser.add_argument('address',
                        help='The GET query URL for your PaperCut Server Health API' +
                        ' (See Options->Advanced->System Health Monitoring)' +
                        ' example: http://203.0.113.0:9191/api/health/?Authorization=authKey1234')

    parser.add_argument('-n', '--name', default=None,
                        help='Filter by name (default none)')

    parser.add_argument('-lo', '--location', default=None,
                        help='Filter by location (default none)')

    parser.add_argument('-s', '--server', default=None,
                        help='Filter by server (default none)')

    parser.add_argument('-li', '--limit', default=250, type=int,
                        help='Maximum number of printers to include in template (default 250)')

    args = parser.parse_args()
    pcUrl = urlparse(args.address)
    main()
