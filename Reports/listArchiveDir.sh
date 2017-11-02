#!/usr/bin/env bash

# For Mac or Linux servers running a Postgrsql database
# Modify to suite

# Displays the location of all print archives for a specific printer,
# for jobs printed after a certain date/time

#  $1  printserver
#  $2  prinnter name
#  $3  date of last run

# For example
#  $ ./getArchiveLocations.sh laptop-serv1 fake_printer "1999-01-08 04:05:06"

# Notes:
#     * to discover the correct path on a Windows system
#       take the value from tbl_printer_usage_log.archive_path & replace '/' with '\'
#     * you must be running an external database to run SQL queries.
#       https://www.papercut.com/kb/Main/RunningPaperCutOnAnExternalDatabase

DATABASE=papercutdb
DBUSER=papercut
DIRSEP='/'

# Are the archives somewhere other than the default?
p="$(~papercut/server/bin/mac/server-command get-config archiving.path)"

if [[ -z "$p" ]] ; then
  p=~papercut/server/data/archive  # Default location
fi

psql -Atqd $DATABASE -U $DBUSER --field-separator=$DIRSEP <<EOF
\set p '$p'
\set server '$1'
\set printer '$2'
\set lastrun '$3'
select :'p',tbl_printer_usage_log.archive_path,tbl_printer_usage_log.job_uid
from tbl_printer_usage_log, tbl_printer
where tbl_printer_usage_log.usage_date > :'lastrun'
and tbl_printer_usage_log.archive_path is not null
and tbl_printer.server_name = :'server'
and tbl_printer.printer_name = :'printer'
and tbl_printer_usage_log.printer_id = tbl_printer.printer_id
EOF

