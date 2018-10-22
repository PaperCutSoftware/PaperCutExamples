# Various scritps and programs that use server-command or web services API.

For more information about using `server-command` or the web services API see our
knowledge base [article](https://www.papercut.com/kb/Main/TopTipsForUsingThePublicWebServicesAPI)
and our [wiki](https://github.com/PaperCutSoftware/PaperCutExamples/wiki).

* `assignPrintersToServerGroups.sh`: Bash script to assign printers to specific group depending on the print server they are attached to
* `allUserInDelegationGroup.sh`: Bash script to add all users into a single internal group for delegation purposes
* `csvListOfPrintersAndFieldValue.sh`: Bash script to print csv list of all printers and the value of a specific property. Defaults to the `disabled` property
* `delete-users-matching-regex`: Small bash script to delete any user whose username matches a regular expression
* `delete-users-matching-regex.ps1`: Small Windows Powershell script to delete any user whose username matches a regular expression
* `displaySharedBalanceWhenAutoChargeToSharedAccount.py`: Lists all users
  who are automatically charging to a shared account and the shared account balance (Python)
* `findAllUsersInDept.py`: Finds all users in a specific department (Python)
* `findAllUsersInGroup.py`: Finds all users in a specific user group (Python)
* `list-shared-account-balances`: Bash script to list all shared accounts and the balance
* `list-shared-account-balances.ps1`: Windows Powershell script to list all shared accounts and the balance
* `list-user-with-no-card-no-1.ps1`: Windows Powershell script to list all users with no primary card number assigned
* `listGroupMembership.sh`: For every user account, list group membership (Bash script)
* `listPrinterStatuses.py`: Python program to show the use of `printer-id` property via the
web services API to streamline using the health interface API
* `loadSharedAcconts.py`: Python program that generates a large file of shared accounts and loads into PaperCut.
  Shows how to use the `getTaskStatus()` method
* `removeTempCardsJob.py`: Removes all temp cards from PaperCut, if the cards are listed in a table.
  Easy to extend to use an external database (Python)
* `removeUsersListedInFile`: Bash script that removes any user _NOT_ listed in a file
* `simpleTopUpBalance`: Small and ugly web application to allow users to top up their PaperCut personal account balance
* `swapCardNumbers.sh`: Bash script to swap the primary-card-number and secondary-card-number fields for all users
* `swapCardNumbers.ps1`: Powershell script to swap the primary-card-number and secondary-card-number fields for all users.
  Note: this script shows how to use the ServerCommandProxy DLL, instead of calling the `server-command` utility
* `topUpOverDrawnAccounts.sh`: Bash script to adjust all -ve balances, presumbly with external funds
* `Update_Card_Number`: Perl script to read usernames and card numbers from csv file and update PaperCut user details with the card number
* `userSelectSharedAccount`: Small and ugly web application to allow users to change their own default shared account
* `../Reports/listArchiveDir.sh`: SQL script to list the archives for a specific printer that have happended since a given date.
  Find it [here](https://github.com/PaperCutSoftware/PaperCutExamples/blob/master/Reports/listArchiveDir.sh)
* `setUserPropeties.php`: A trival PHP 7 example that shows how to handle encoding more complex paramters
* `C/xmlrpc.c`: The basics of calling PaperCut web services from C. Inclues a Makefile to help you build the example code

Note:
* If you are using the Perl scripting language to interface with PaperCut APIs
  then use the Data::Dumper module to help understand the data
  you get from PaperCut (and how your language library is presenting the information).

  More information on this module at http://perldoc.perl.org/Data/Dumper.html
