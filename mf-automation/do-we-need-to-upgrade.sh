#!/bin/dash

# Use the Dash shell. It's smaller and faster

# 1. Discover the latest PaperCut MF release version fron the Atom feed
# 2. Discover what version of PaperCut MF we are running
# 3. If they are not the same then create a job ticket, but only if we have not seen this release before

# This example uses xmllint, jq and the glab (the GitLab command line client). They will need to be installled

API_TOKEN="$(cat ~/.PAPERCUT_API_TOKEN)"  # Dont' hard code API tokens
MF_HOST="$(hostname).local" # Modify to suit
LAST_VERSION_CHECKED="0.0.0" # Default to never checked
PRODUCT=mf # Changing to "ng" should work, but has not been tested

if [ -e ~/.PAPERCUT_LAST_VERSION_CHECKED ] ; then
  LAST_VERSION_CHECKED=$(cat ~/.PAPERCUT_LAST_VERSION_CHECKED)
fi

echo last version checked is $LAST_VERSION_CHECKED

# Discover the latest PaperCut MF release from the papercut.com atom feed
# Note: Using an older version of xmllint so sed needs to add a new line to each version line
CURRENT_RELEASE=$(curl -sL http://www.papercut.com/products/$PRODUCT/release-history.atom |
xmllint --xpath "//*[local-name()='feed']/*[local-name()='entry']/*[local-name()='id']/text()" - |
sed -Ene 's/tag:papercut.com,[0-9]+-[0-9]+-[0-9]+:'$PRODUCT'\/releases\/v([0-9]+)-([0-9]+)-([0-9]+)/\1.\2.\3\
/gp' |
sort -rV | head -1)

echo $CURRENT_RELEASE > ~/.PAPERCUT_LAST_VERSION_CHECKED

if [ "$LAST_VERSION_CHECKED" = "$CURRENT_RELEASE" ] ; then
  echo No new release
#  exit 0
fi

echo Found a new release.

# We need the health API key. Get via the web services API. Config health.api.key
HEALTH_API_KEY=$(curl -s -H "content-type:text/xml"  "http://${MF_HOST}:9191/rpc/api/xmlrpc" --data  @-  <<EOF | xmllint --xpath '//*/value/text()' -
<?xml version="1.0"?>
<methodCall>
<methodName>api.getConfigValue</methodName>
<params>
<param>
<value>${API_TOKEN}</value>
</param>
<param>
<value>health.api.key</value>
</param>
</params>
</methodCall>
EOF
)

# If running on the PaperCut MF server this approach is much easier
# HEALTH_API_KEY=$(~papercut/server/linux-x64/bin/server-command get-config-value health.api.key)

if [ -z "$HEALTH_API_KEY" ] ; then
  echo HEALTH_API_KEY not found
  exit 1
fi

INSTALLED_RELEASE=$(curl -s -H "Authorization:$HEALTH_API_KEY" "http://${MF_HOST}:9191/api/health" | jq '.applicationServer.systemInfo.version' |sed -Ee 's/^"([0-9]+\.[0-9]+\.[0-9]+).+$/\1/')

if [ "$INSTALLED_RELEASE" = "$CURRENT_RELEASE" ] ; then
  echo No new release, $INSTALLED_RELEASE is up to date
#  exit 0
fi

echo Installed Release is $INSTALLED_RELEASE, $CURRENT_RELEASE is now avaliable. Upgrade possible

MAJOR="$(echo $CURRENT_RELEASE  | cut -d . -f 1)"
MINOR="$(echo $CURRENT_RELEASE  | cut -d . -f 2)"
PATCH="$(echo $CURRENT_RELEASE  | cut -d . -f 3)"

RELEASE_NOTES="https://www.papercut.com/products/$PRODUCT/release-history/${MAJOR}-${MINOR}/#v${MAJOR}-${MINOR}-${PATCH}"

MINION=alecthegeek

# Need to install a repo client to create job ticket, or use appropriate API on your ticket system
glab issue create -a $MINION -t "Investigate Possible PaperCUt $(echo $PRODUCT | tr [a-z] [A-Z]) upgrade to version $CURRENT_RELEASE" -d "Review release notes at $RELEASE_NOTES.
Note installed release is $INSTALLED_RELEASE"
