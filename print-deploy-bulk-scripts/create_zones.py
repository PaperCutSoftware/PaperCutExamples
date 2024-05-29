#
# (c) Copyright 1999-2024 PaperCut Software International Pty Ltd.
#

import requests
import csv
import argparse
import json
import sys

# Suppress warnings for self-signed certificates. Remove this code in environments where CA-signed certificates are used. 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#The script will default to these values are not specified. Don't edit these in the script, rather provide them through input arguments. Run "python 3 create_zones.py --help"
host_name = 'localhost' 
port = 9192
password = "password"
username = "admin"

#Global variables
session = None

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

def read_list_from_string(input_string):
    #Check if empty string or only spaces
    if input_string.strip() == '':
        return []
    # Check if a comma exists in the input string
    if ',' in input_string:
        # Split the string on commas and return the list of strings
        return input_string.split(',')
    else:
        # If no comma exists, return the original string in a list
        return [input_string]


if __name__ == "__main__":

    # Create the argument parser
    parser = argparse.ArgumentParser(description='Create zones based on CSV.')

    # Add input arguments
    parser.add_argument('-e', '--edit', action='store_true', help='If -e or --edit argument is present, then zones will be updated with the CSV configuration. Otherwise the existing zones will be skipped.')
    parser.add_argument('-p', '--password', type=str, help='Password for authentication')
    parser.add_argument('-u', '--username', type=str, help='Username for authentication')
    parser.add_argument('-P', '--port', type=int, help='Port number for the connection')
    parser.add_argument('--host', type=str, help='Port number for the connection')

    # Add two required positional arguments
    parser.add_argument('csv_file_path', type=str, help='The CSV input file to process')

    # Parse the command line arguments
    args = parser.parse_args()

    # Check that we at least have a CSV filename.
    if args.csv_file_path:
        print(f"Input CSV file provided: {args.csv_file_path}")
    
    else:
        print("Required argument 'csv_file_path' was not provided. At a minimum, run 'python3 zones.csv' if your file is zones.csv.")
        sys.exit(1)

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
        port = port
    else:
        print("Port not set. Using 9192 as default port. Set port with --port input argument.'")

    if not login(username,password):
        print("Exiting: Couldn't login")
        sys.exit(1)
    #############

    #Retrieve zones
    existing_zones = get_data("/print-deploy/admin/api/zones")

    # Read data from the CSV file
    with open(args.csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            zonename = row['Zone Name']
            displayname = row['Display Name']
            groups = read_list_from_string(row['Groups'])
            ipRange = read_list_from_string(row['IP Range'])
            hostnameRegex = row['Hostname Regex']

            #Prep data that will be posted to Print Deploy to create or edit a zone
            data = {
                    'groups': groups,
                    'ipRange': ipRange,
                    'name': row['Zone Name'],
                    'displayName': row['Display Name']
            }
            #Check if hostname regex exists, only then include it in the data. 
            if hostnameRegex.strip() != '':
                data['hostnameRegex'] = hostnameRegex

            zone_already_exists = any(zone.get('name') == zonename for zone in existing_zones)
            if zone_already_exists and args.edit:
                print(f"Editing '{zonename}' as it already exists and '-e' or '--edit' argument was set. ")
                #Get existing zone ID for zone with matching name
                matching_zones = filter(lambda d: 'name' in d and d['name'] == zonename, existing_zones)
                zone_id = (next(matching_zones, None)).get('id')

                # Send the POST request
                post_data("/print-deploy/admin/api/zones/{}".format(zone_id),data)
            #Skipping zone
            elif zone_already_exists:
                print(f"Skipping '{zonename}' as it already exists. If you want to edit the zone instead, run the script with '-e' argument.")
            #Create new zone
            else:
                print(f"Creating zone '{zonename}'.")

                # Send the POST request
                post_data("/print-deploy/admin/api/zones",data)

