#!/usr/bin/env bash

# If a user is to be allowed to be a delegate for all users in an organisation
# it would be useful to add the "[All Users]" group to the list. However you
# can't do this as it's not a real group.

# There is a workaround. Create a real group that has all PaperCut users in it.
# If you can't do this in your directory source then this can be automatically
# done using a script (like this one) run every couple of hours for instance
# on the PaperCut server.

# The script needs write permission to the appropriate location)

# Note that his example will overwrite any current contents.
# If you want to preserver existing information in the file then
# you will need something more sophisticated.

# See also https://www.papercut.com/kb/Main/InternalGroups

server-command list-user-accounts | xargs -I {} echo "AllUser:{}" > ~papercut/server/data/conf/additional-groups.txt

