import requests
import csv
import sys
import json

#Update these. Only implemented this script for HTTP as an example
host_name = 'localhost' 
port = 9191

#Global variables
session = None

def login():
    #Get SessionID
    global session 
    session = requests.Session()
    # First request to get the session cookies
    response = session.get("http://{}:{}/admin".format(host_name,port))

    # Define the URL
    url = 'http://{}:{}/app'.format(host_name,port)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "localhost:9191",
        "Referer": "http://{}:{}/admin".format(host_name,port),
    }


    # Define the request body
    body = {
        "service": "direct/1/Home/$Form",
        "sp": "S0",
        "Form0": "$Hidden$0,$Hidden$1,inputUsername,inputPassword,$Submit$0,$PropertySelection",
        "$Hidden$0": "true",
        "$Hidden$1": "X",
        "inputUsername": "admin",
        "inputPassword": "password",
        "$Submit$0": "Log in",
        "$PropertySelection": "en"
    }

    response = session.post(url, headers=headers, data=body)

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
    url = 'http://{}:{}{}'.format(host_name,port,path) 

    # Define the headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = session.get(url, headers=headers)
    # Check the response
    if response.status_code == 200:
        return response.json()   
    else:
        print("Request to '{}' failed with status code {}".format(path,response.status_code))
        return False

def post_data(path,data):
#############

# Define the URL
    url = 'http://{}:{}{}'.format(host_name,port,path) 

    # Define the headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    response = session.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200 or response.status_code == 302:
        return True  
    else:
        print("Request to '{}' failed with status code {}".format(path,response.status_code))
        return False


if __name__ == "__main__":
    # Check the number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 assign_print_queues_to_zone.py print_queue_name zone_name")
        sys.exit(1)
    new_print_queue_name = sys.argv[1] 
    zone_name = sys.argv[2]

    zone_id = None
    printers_ids = {}
    zone={}
    zone_print_queues = []

    if not login():
        print("Exiting: Couldn't login")
        sys.exit(1)

    #Retrieve all printer IDS    
    printers = get_data("/print-deploy/admin/api/printQueues")
    for i in printers:
        printers_ids[i["name"]]=i["key"]

    #Retrieve zones and connected print queues
    zones = get_data("/print-deploy/admin/api/zones")

    for zone in zones:
        if zone["name"] == zone_name:
            print("Found zone {}".format(zone_name))
            zone_id = zone["id"]
            zone_print_queues = zone["zonePrintQueues"]
            is_print_queue_already_connected = False
            for print_queue in zone_print_queues:
                if print_queue.get("key") == printers_ids.get(new_print_queue_name):
                    print("Printer {} is already deployed to {}.".format(new_print_queue_name,zone_name))
                    is_print_queue_already_connected = True
            if not is_print_queue_already_connected:
                print("Deploying printer {} to {}.".format(new_print_queue_name,zone_name))
                zone_print_queues.append({'key': printers_ids[new_print_queue_name], 'optional': True, 'defaultPrinter': False})

            payload = {"printQueues":zone_print_queues}
            post_data("/print-deploy/admin/api/zones/{}/printQueues".format(zone_id),payload)






