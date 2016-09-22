# PaperCut PRTG Template Generator
### Features
Creates [device templates](https://www.paessler.com/manuals/prtg/create_device_template) for your [PRTG Network Monitoring Tool](https://www.paessler.com/prtg) that you can use to monitor your server's specific PaperCut installation.

##### Statistics monitored:
* Server health status
  * Overall server health
  * Current number of held jobs
  * Pages printed in the last minute
  * Server errors in the last 10 minutes
  * Server warnings in the last 10 minutes
* Individual printer health status
* Individual device health status

##### For more information, see:

* [Simple Health Monitoring with PRTG](https://www.papercut.com/kb/Main/SimpleMonitorPRTG)
* [Advanced Health Monitoring with PRTG](https://www.papercut.com/kb/Main/AdvancedMonitorPRTG)
* [PaperCut's Health Monitoring API Reference](https://www.papercut.com/products/ng/manual/common/topics/tools-monitor-system-health-api-overview.html)
* [PRTG User Manual](https://www.paessler.com/manuals/prtg) for more information.


### Requirements
* Python 3.1

### Running the Script

1. In the PaperCut Admin web interface, select `Options > Advanced`

2. In the System Health Monitoring area, copy the URL for the PaperCut Health Monitoring API

3. Run the script with the first argument being the GET Query Parameter (the Health Monitoring URL) for the PaperCut Health Monitoring API.
```shell
./pc-prtg-generator.py http://203.0.113.0:9191/api/health/?Authorization=authKey1234 -s linux1 -lo office1
```
```shell
python3 pc-prtg-generator.py http://203.0.113.0:9191/api/health/?Authorization=authKey1234 --limit 50
```
This will generate files in the script's directory that are specific for your PaperCut Installation. which You can then be used these files as templates in the PRTG Admin interface., specific for your PaperCut Installation.

4. Copy the files to your `{PRTG_INSTALLATION}\devicetemplates` directory.



### Required Arguments
Argument | Parameter | Description
---|---|---
`address`|STRING|GET Query URL for your PaperCut Server Health Monitoring API
### Optional Arguments
Argument | Parameter | Description
---|---|---
`-n` `--name`|STRING (Default None)|Filter results by name
`-lo` `--location`|STRING (Default None)|Filter results by location
`-s` `--server` |STRING (Default None)|Filter results by server
`-li` `--limit`|INT (Default 250)|Maximum number of printers/devices to include in the template
### Notes
* PaperCut System Health URLs are currently hard coded, so PRTG's [Smart URL Replacement](https://www.paessler.com/manuals/prtg/http_advanced_sensor#smart) is not configured. If your server address updates to a new one, you need to run the script again.
