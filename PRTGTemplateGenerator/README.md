# PaperCut PRTG Template Generator
### Features
Creates device templates for your [PRTG Network Monitoring Tool](https://www.paessler.com/prtg), in order to monitor, and detect potential errors on your server's specific PaperCut installation using [PaperCut's Health Monitoring API](https://www.papercut.com/products/ng/manual/common/topics/tools-monitor-system-health-api-overview.html).

##### Statistics monitored:
* Server Health Status
  * Overall Server Health
  * Current Number of Held Jobs
  * Pages Printed in the last minute
  * Server Errors in the last 10 minutes
  * Server Warnings in the last 10 minutes
* Individual Printer Health Statuses
* Individual Device Health Statuses

Please refer to PaperCut articles [Simple Health Monitoring with PRTG](https://www.papercut.com/kb/Main/SimpleMonitorPRTG), [Advanced Health Monitoring with PRTG](https://www.papercut.com/kb/Main/AdvancedMonitorPRTG), [PaperCut's Health Monitoring API Reference](https://www.papercut.com/products/ng/manual/common/topics/tools-monitor-system-health-api-overview.html) and the [PRTG User Manual](https://www.paessler.com/manuals/prtg) for more information.


### Requirements
* Python 3.1

### Running the Script
Run the script with the first argument being the `GET Query Parameter` (the Health Monitoring URL) for the PaperCut Health Monitoring API.

You can find the Health Monitoring URL in the Admin UI, under `Options > Advanced > System Health Monitoring`.
```shell
./pc-prtg-generator.py http://203.0.113.0:9191/api/health/?Authorization=authKey1234 -s linux1 -lo office1
```
```shell
python3 pc-prtg-generator.py http://203.0.113.0:9191/api/health/?Authorization=authKey1234 --limit 50
```

This will generate files in the script's directory which can then be used as templates in the PRTG Admin interface, specific for your PaperCut Installation. (Copy the files to your  `{PRTG_INSTALLATION}\devicetemplates` directory).


### Required Arguments
Argument | Parameter | Description
---|---|---
`address`|STRING|GET Query URL for your PaperCut Server Health Monitoring API
### Optional Arguments
Argument | Parameter | Description
---|---|---
`-n` `--name`|STRING (Default None)|Filter results by Name
`-lo` `--location`|STRING (Default None)|Filter results by Location
`-s` `--server` |STRING (Default None)|Filter results by Server
`-li` `--limit`|INT (Default 250)|Maximum number of printers/devices to include in the template
### Notes
* URLs are currently hardcoded, and won't use PRTG's [Smart URL Replacement](https://www.paessler.com/manuals/prtg/http_advanced_sensor#smart). If your server address updates to a new one, you will need to run the script again.
