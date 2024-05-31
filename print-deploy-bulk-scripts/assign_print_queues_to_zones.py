#
# (c) Copyright 1999-2024 PaperCut Software International Pty Ltd.
#

import requests
import csv
import argparse
import sys
import json


#Global variables
session = None
printers_ids = None
zones = None


# Suppress warnings for self-signed certificates. Remove this code in environments where CA-signed certificates are used. 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#The script will default to these values are not specified. Don't edit these in the script, rather provide them through input arguments. Run "python 3 create_zones.py --help"
host_name = 'localhost' 
port = 9192
password = "password"
username = "admin"

def login(username,password):
    #Get SessionID
    global session 
    session = requests.Session()
    # First request to get the session cookies
    response = session.get("https://{}:{}/admin".format(host_name,port), verify=False)

    # Define the URL
    url = 'https://{}:{}/app'.format(host_name,port)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "{}:{}".format(host_name,port),
        "Referer": "https://{}:{}/admin".format(host_name,port),
    }


    # Define the request body
    body = {
        "service": "direct/1/Home/$Form",
        "sp": "S0",
        "Form0": "$Hidden$0,$Hidden$1,inputUsername,inputPassword,$Submit$0,$PropertySelection",
        "$Hidden$0": "true",
        "$Hidden$1": "X",
        "inputUsername": username,
        "inputPassword": password,
        "$Submit$0": "Log in",
        "$PropertySelection": "en"
    }

    response = session.post(url, headers=headers, data=body, verify=False)

    # Check the response
    if response.status_code == 200 or response.status_code == 302:
        # Check if the response contains the string "Login"
        if "Login" in response.text:
            print("Username or password not correct")
            return False
        else:
            print("Login was successful")
            return True
    else:
        print("Request failed with status code %s" % response.status_code)
        return False


def get_data(path):

#############

# Define the URL
    url = 'https://{}:{}{}'.format(host_name,port,path) 

    # Define the headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = session.get(url, headers=headers, verify=False)
    # Check the response
    if response.status_code == 200:
        return response.json()   
    else:
        print("Request to '{}' failed with status code {}".format(path,response.status_code))
        return False

def post_data(path,data):
#############

# Define the URL
    url = 'https://{}:{}{}'.format(host_name,port,path) 

    # Define the headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = session.post(url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200 or response.status_code == 302 or response.status_code == 201:
        return True  
    else:
        print("Request to '{}' failed with status code {}".format(path,response.status_code))
        return False

# Assign print queue to Zone
def connect_print_queue_to_zone(zone_name, new_print_queue_name, optional, edit=False):
    global zones
    global printers_ids

    for zone in zones:
        if zone["name"] == zone_name:
            print("Found zone {}".format(zone_name))
            zone_id = zone["id"]
            zone_print_queues = zone["zonePrintQueues"]
            is_print_queue_already_connected = False
            
            # Check if the print queue already exists in the zone
            for i, print_queue in enumerate(zone_print_queues):
                if print_queue.get("key") == printers_ids.get(new_print_queue_name):
                    is_print_queue_already_connected = True
                    if edit:
                        # Replace the matching print queue
                        print("Editing printer {} in {}.".format(new_print_queue_name, zone_name))
                        zone_print_queues[i] = {'key': printers_ids[new_print_queue_name], 'optional': optional, 'defaultPrinter': False}
                    else:
                        print("Printer {} is already deployed to {}.".format(new_print_queue_name, zone_name))
                    break

            if not is_print_queue_already_connected:
                print("Deploying printer {} to {}.".format(new_print_queue_name, zone_name))
                zone_print_queues.append({'key': printers_ids[new_print_queue_name], 'optional': optional, 'defaultPrinter': False})

            payload = {"printQueues": zone_print_queues}
            post_data("/print-deploy/admin/api/zones/{}/printQueues".format(zone_id), payload)
            break

#Export current print queue to zone config
def export_print_queues_and_zones(output_file):
    global zones 
    global printers_ids
    
    # Reverse the printer_ids dictionary for easy lookup
    printer_keys = {v: k for k, v in printers_ids.items()}

    # Track assigned printers
    assigned_printers = set()

    # Prepare CSV data
    csv_data = [["Zone Name", "Print Queue", "Optional"]]

    for zone in zones:
        zone_name = zone['name']
        for pq in zone['zonePrintQueues']:
            if pq['key'] in printer_keys:
                print_queue = printer_keys[pq['key']]
                optional = "True" if pq.get('optional', False) else ""
                csv_data.append([zone_name, print_queue, optional])
                assigned_printers.add(pq['key'])
        if not zone['zonePrintQueues']:
            csv_data.append([zone_name, "", ""])

    # Add unassigned printers
    unassigned_printers = sorted(set(printers_ids.values()) - assigned_printers)
    for printer_key in unassigned_printers:
        printer_name = printer_keys.get(printer_key, '')
        csv_data.append(["", printer_name, ""])

    # Write to CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

if __name__ == "__main__":


    # Create the argument parser
    parser = argparse.ArgumentParser(description='Create zones based on CSV.')

    # Add input arguments
    parser.add_argument('-p', '--password', type=str, help='Password for authentication')
    parser.add_argument('-u', '--username', type=str, help='Username for authentication')
    parser.add_argument('-P', '--port', type=int, help='Port number for the connection')
    parser.add_argument('--host', type=str, help='Port number for the connection')
    parser.add_argument('-f','file', type=str, help='The CSV input file to process.')
    parser.add_argument('--output', type=str, help='Download CSV file with current print queue assignment. Useful to edit and import again.')
    parser.add_argument('--printer', help='If --printer argument is present, a single printer will be assigned to to the zone specified by --zone. ')
    parser.add_argument('-z','--zone', help='The zone the single printer (--printer) will be connected to.')
    parser.add_argument('-o','--optional',action='store_true',help='If set, then the single printer (--printer) will be connected to the zone (--zone) as optional. ')
    parser.add_argument('-e','--edit',action='store_true',help='If set, then the optional flag will be updated if a print queue is already deployed to a zone.')

    # Parse the command line arguments
    args = parser.parse_args()

    #Default password to "password" if not set
    if args.password:
        password = args.password
    else:
        print("Password not set. Using 'password' as default password. Set password with --password input argument.")

    #Default username to "admin" if not set
    if args.username:
        username = args.username
    else:
        print("Username not set. Using 'admin' as default username. Set username with --username input argument.")

    #Default host to "localhost" if not set
    if args.host:
        host_name = args.host
    else:
        print("Host not set. Using 'localhost' as default host. Set host with --host input argument.'")

    #Default port to "9192" if not set
    if args.port:
        port = args.port
    else:
        print("Port not set. Using 9192 as default port. Set port with --port input argument.'")

    #Setting optional variable. This won't be used for a CSV import, only when one specific print queue is imported. 
    optional = args.optional

    #If set, then the optional flag will be updated if a print queue is already deployed to a zone.
    edit = args.edit

    zone_id = None
    printers_ids = {}
    zone_print_queues = []


    if not login(username,password):
        print("Exiting: Couldn't login")
        sys.exit(1)
    #############

    #Retrieve zones and connected print queues
    zones = get_data("/print-deploy/admin/api/zones")

    #Retrieve all printer IDS    
    printers = get_data("/print-deploy/admin/api/printQueues")
    for i in printers:
        printers_ids[i["name"]]=i["key"]

    #Export current config 
    if args.output:
        export_print_queues_and_zones(args.output)

    #If print queue name and zone are provided through arguments
    if args.printer and args.zone:
        new_print_queue_name = args.printer 
        zone_name = args.zone
        connect_print_queue_to_zone(zone_name,new_print_queue_name,optional,edit)

    #If CSV file provided
    if args.file:
        csv_file_path = args.file
        print(f"Processing file '{csv_file_path}'")
        # Read data from the CSV file
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                zone_name = row['Zone Name'].strip()
                new_print_queue_name = row['Print Queue'].strip()
                optional = row['Optional'].strip().lower() == 'true'
                #Check if zone name and print queue name not empty. 
                if zone_name and new_print_queue_name: 
                    connect_print_queue_to_zone(zone_name,new_print_queue_name,optional,edit)            








