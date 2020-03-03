# Locate a user on something other than the username

When using server command users are identified by their username. This is guaranteed to be unique.

But sometimes it would be useful find user accounts based on other attributes, such as full name or card number

The card number is easy. Use `look-up-user-name-by-card-no` sub command of `server-command`. However things like the
user's full name are a little harder.

The following approach will be slow but does work. It uses the features of the Bash shell, but the same
approach is possible with the Windows PowerShell as well.

The script `getPPCuserName.sh` will take the name of attribute and a value. It will then return of username
of the account that matches. However be careful, as it could be zero accounts or more than one. It will be slow as it
looks at each user account in turn until it finds a match.

For example

`server-command adjust-user-account-balance $(./getPPCuserName.sh full-name "Alec Clews") 30 'Add $30 to user Alec Clews' default`

