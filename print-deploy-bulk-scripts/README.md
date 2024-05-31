# Introduction #
These Python scripts can be used to create zones in Print Deploy and assign print queues to these zones. 

### Requirements ###
* [Python3](https://www.python.org/downloads/)
* [Python requests](https://pypi.org/project/requests/)


# How to create zones #
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

# How to assign print queues to zones #
Reference the zones.csv exmaple in this repo, or download your current zones and print queues to a CSV file by running:
`python3 assign_print_queues_to_zones.py --output output.csv`

This output CSV file will be compatible to import again. At the bottom of the CSV file print queues will be listed that are not yet connected to any zones. To assign them to zones, simply fill in the zone name and then run:

`python3 assign_print_queues_to_zones.py -f input.csv --edit` (In this example, the input file was renamed to input.csv)

Don't edit the headings for the following columns:

* Zone Name: Which zone to connect the print queue to.
* Print Queue: The print queue name to connect
* Optional: If set to 'true', then this print queue will be connected as optional to the zone. 

### How to run script ###
Example when importing from a CSV file. This example will update the Optional value if the print queue was already deployed: `python3 assign_print_queues_to_zones.py -f printers_to_zones_example.csv --edit`

### Optional Arguments ###
Choose whether you'll import the print queue to zone assignment from a CSV, or provide a single print queue via arguments.

| Option                      | Description                                                                                           |
|-----------------------------|-------------------------------------------------------------------------------------------------------|
| `-p, --password` | Password for authentication                                                                                      |
| `-u, --username` | Username for authentication                                                                                      |
| `-P, --port`      | Port number for the connection                                                                                  |
| `--host`               | Host name for the connection                                                                               |
| `-f, --file`      | The CSV input file to process.                                                                                  |
| `--output`      | Download CSV file with current print queue assignment. Useful to edit and import again.                       |
| `--printer`         | If `--printer` argument is present, a single printer will be assigned to the zone specified by `--zone`.      |
| `-z, --zone`      | The zone the single printer (`--printer`) will be connected to.                                                 |
| `-o, --optional`            | If set, then the single printer (`--printer`) will be connected to the zone (`--zone`) as optional.   |
| `-e, --edit`                | If set, then the optional flag will be updated if a print queue is already deployed to a zone.        |
