# Various scritps and programs that use server-command or web services API.

For more information about using `server-command` or the web services API see our
knowledge base [article](https://www.papercut.com/kb/Main/TopTipsForUsingThePublicWebServicesAPI).

* Update_Card_Number: Perl script to read usernames and card numbers from csv file and update PaperCut user details with the card number
* delete-users-matching-regex: Small bash script to delete any user whose username matches a regular expression
* delete-users-matching-regex.ps1: Small Windows Powershell script to delete any user whose username matches a regular expression
* displaySharedBalanceWhenAutoChargeToSharedAccount.py: Lists all users who are automatically charging to a shared account and the shared account balance (Python)
* findAllUsersInDept.py: Finds all users in a specific department (Python)
* findAllUsersInGroup.py: Finds all users in a specific user group (Python)
* list-shared-account-balances: Bash script to list all shared accounts and the balance
* loadSharedAcconts.py: Python program that generates a large file of shared accounts and loads into PaperCut. Shows how to use the `getTaskStatus()` method
* removeTempCardsJob.py: Removes all temp cards from PaperCut, if the cards are listed in an table. Easy to extend to use an external database (Python)
* removeUsersListedInFile: Bash script that removes any user _NOT_ listed in a file
* simpleTopUpBalance: Small and ugly web application to allow users to top up their PaperCut personal account balance
* swapCardNumbers.sh: Bash script to swap the primary-card-number and secondary-card-number fields for all users.
* userSelectSharedAccount: Small and ugly web application to allow users to change their own default shared account
* ../Reports/listArchiveDir.sh: SQL script to list the archives for a specific printer that have happended since a given date. Find it [here](https://github.com/PaperCutSoftware/PaperCutExamples/blob/master/Reports/listArchiveDir.sh)
* setUserPropeties.php: A trival PHP 7 example that shows how to handle encoding more complex paramters
* C/xmlrpc.x: The basics of calling PaperCut web services from C. Inclues a Makefile to help you build it

