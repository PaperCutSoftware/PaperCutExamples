#!/usr/bin/env bash

# For Mac or Linux servers running a Postgrsql database
# Modify to suite

# Deletes user accounts after a fixed period if the user name matches a mask

#  $1  Period
#  $2  Name Mask  optional

# For example
#  $ ./deleteUsersAfterPeriod.sh  '1 Year'  'Guest-*'

# Notes:
#     * to discover the correct path on a Windows system
#       take the value from tbl_printer_usage_log.archive_path & replace '/' with '\'
#     * you must be running an external database to run SQL queries.
#       https://www.papercut.com/kb/Main/RunningPaperCutOnAnExternalDatabase

DATABASE=papercutdb
DBUSER=papercut

p=${1:?'Must provide a period length, e.g. "1 Year"'}
m=${2:-"%"}

psql -Abatqd $DATABASE -U $DBUSER --set=period=$p --set=userMask=$m <<EOF
select 'server-command delete-user ', tbl_user.user_name
from tbl_user
where tbl_user.created_date + interval :period < current_date
and tbl_user.deleted = 'N'
and tbl_user.user_name like :'userMask';
EOF

