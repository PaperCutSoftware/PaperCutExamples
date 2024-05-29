# Introduction #
These Python scripts can be used to create zones in Print Deploy and assign print queues to these zones. 

### Requirements ###
* [Python3](https://www.python.org/downloads/)
* [Python requests](https://pypi.org/project/requests/)


## How to create zones ##
See the example zones.csv file. 

Don't edit the headings. 

* Zone Name: The name that will appear in the admin interface
* Display Name (Optional): Optional display name for users. If this column is left blank, then users will be presented with the Zone Name instead. 
* Groups (Optional): If left blank, then this zone will be available to all groups. If more than one group is needed, then use a comma seperated list within quotes. For example: "group1,group2". 
* IP Range (Optional): If left blank, then this zone will be available to all IP addresses. If more than one range is needed, then use a comma seperated list within quotes. For example: "192.168.1.1-192.168.1.10,192.168.0.0/24". 
* Hostname Regex: Hostname regex string. See example strings [here](https://www.papercut.com/help/manuals/print-deploy/set-up/add-zones-user-groups/)


### How to run script ###
Example for Mac/Linux: `python3 ./create_zones.py zones.csv --username admin --password password --host localhost --port 9192 -e`   
Example for Windows: `create_zones.py zones.csv --username admin --password password --host localhost --port 9192 -e` 

### Positional Arguments ###

| Argument       | Description                          |
| -------------- | ------------------------------------ |
| `csv_file_path`| The CSV input file to process        |

### Optional Arguments ###

| Option                          | Description                                                                 |
| ------------------------------- | --------------------------------------------------------------------------- |
| `-e`, `--edit`                  | If `-e` or `--edit` argument is present, then zones will be updated with the CSV configuration. Otherwise the existing zones will be skipped. |
| `-p`, `--password` | Password for authentication. If not set, then 'password' is used.                                              |
| `-u`, `--username` | Username for authentication. If not set, then 'admin' is used.                                               |
| `-P`, `--port`        | Port number for the connection. If not set, then '9192' is used.                                              |
| `--host`                   | Host address for the connection. If not set, then 'localhost' is used. |

