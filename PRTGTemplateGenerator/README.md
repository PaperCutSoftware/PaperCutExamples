# PaperCut PRTG Template Generator

### Requirements
* Python 2.7

### Running the Script
Run the script with the first argument being the `GET Query Parameter` for the PaperCut Health Monitoring API.

You can find the Health Monitoring URL in the Admin UI, under `Options > Advanced > System Health Monitoring`.
```shell
./pc-prtg-generator.py 'http://203.0.113.0:9191/api/health/?Authorization=authKey1234' -s linux1 -lo office1
```
```shell
python pc-prtg-generator.py 'http://203.0.113.0:9191/api/health/?Authorization=authKey1234' --limit 50
```
This will generate files in the script's directory which can then be used as templates in the PRTG Admin interface, specific for your PaperCut Installation.

### Required Arguments
Argument | Parameter | Description
---|---|---
`address`|STRING|GET Query URL for your PaperCut Server Health Monitoring API
### Optional Arguments
Argument | Parameter | Description
---|---|---
`-lo` `--location`|STRING (Default None)|Filter results by Location
`-s` `--server` |STRING (Default None)|Filter results by Server
`-li` `--limit`|INT (Default 250)|Maximum number of printers/devices to include in the template
