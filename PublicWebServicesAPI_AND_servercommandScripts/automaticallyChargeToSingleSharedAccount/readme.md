In PaperCut NG or MF, you have the option to charge all of the activity performed by a specific user to a single shared account. This option can be found under **Users** > **<select-user>** > **Account Selection**.
Once this option is selected, a specific shared account can be specified for user activity to be charged against. 

This PowerShell example uses our server-command utility to set this setting for specific users as specified in an accompanying CSV file. 
For more information on server-command, see https://www.papercut.com/help/manuals/ng-mf/common/tools-server-command/

The PowerShell script should be adjusted on line 6 to specify the location of your input CSV file.

The CSV file should be in the following format:
| username | account   |
| -------- | --------- |
| ann      | Biology   |
| betty    | Chemistry |
| donna    | Drama     |
| harold   | English   |
| jane     | French    |

This script is designed to be executed on the PaperCut NG or MF Application Server
