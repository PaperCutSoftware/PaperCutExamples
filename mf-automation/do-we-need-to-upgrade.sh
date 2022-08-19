#!/bin/dash

# Use the Dash shell. It's smaller and faster

# 1. Discover the latest PaperCut MF release version fron the Atom feed
# 2. Discover what version of PaperCut MF we are running
# 3. If they are not the same then create a job ticket, but only if we have not seen this release before

# This example uses xmllint, jq and the glab (the GitLab command line client). They will need to be installled

MF_HOST="$(hostname).local" # Modify to suit
PRODUCT=mf # Changing to "ng" should work, but has not been tested
PRODUCT_UPCASE=$(echo $PRODUCT | tr [a-z] [A-Z]) # Sometimes we need upper case version
GH_REPO="PaperCutSoftware/PaperCutExamples"

# ID of system admin to review releases
MINION=alecthegeek


# We need the config health.api.key value
# Assume we are on the PaperCut MF server and use server-command (NB Needs to run under the correct user)
if ! HEALTH_API_KEY=$(~papercut/server/linux-x64/bin/server-command get-config-value health.api.key) ; then

  # Can't use server-command. Get via it the web services API.

  # Need a web services API token.Get this from your local PaperCut admin 
  API_TOKEN="$(cat ~/.PAPERCUT_API_TOKEN)"  # Dont' hard code API tokens

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
fi

if [ -z "$HEALTH_API_KEY" ] ; then
  echo HEALTH_API_KEY not found
  exit 1
fi

INSTALLED_RELEASE=$(curl -s -H "Authorization:$HEALTH_API_KEY" "http://${MF_HOST}:9191/api/health" | jq '.applicationServer.systemInfo.version' |sed -Ee 's/^"([0-9]+\.[0-9]+\.[0-9]+).+$/\1/')

# Discover the latest PaperCut MF release from the papercut.com atom feed
CURRENT_RELEASE=$(curl -sL http://www.papercut.com/products/$PRODUCT/release-history.atom |
  xmllint --xpath "//*[local-name()='feed']/*[local-name()='entry'][1]/*[local-name()='id']/text()"  - |
  sed -Ene 's/tag:papercut.com,[0-9]{4}-[0-9]{2}-[0-9]{2}:'$PRODUCT'\/releases\/v([0-9]+)-([0-9]+)-([0-9]+)/\1.\2.\3/gp')

echo Latest PaperCut release is $CURRENT_RELEASE. Installed Release is $INSTALLED_RELEASE

#Default
LAST_VERSION_CHECKED=$INSTALLED_RELEASE

if [ -e ~/LAST_VERSION_CHECKED ] ;then
  LAST_VERSION_CHECKED=$(cat ~/LAST_VERSION_CHECKED) # Override default
fi

if [ "$LAST_VERSION_CHECKED" = "$CURRENT_RELEASE" ] ; then
  echo PaperCut $PRODUCT_UPCASE $CURRENT_RELEASE  already checked. Nothing to do here
  exit 0
fi

if [ "$INSTALLED_RELEASE" = "$CURRENT_RELEASE" ] ; then
  echo Installed release $INSTALLED_RELEASE is already up to date. No new update available 
  exit 0
fi

echo PaperCut $PRODUCT_UPCASE $INSTALLED_RELEASE can be upgraded to $CURRENT_RELEASE

MAJOR="$(echo $CURRENT_RELEASE  | cut -d . -f 1)"
MINOR="$(echo $CURRENT_RELEASE  | cut -d . -f 2)"
FIX="$(echo $CURRENT_RELEASE  | cut -d . -f 3)"

RELEASE_NOTES="https://www.papercut.com/products/$PRODUCT/release-history/${MAJOR}-${MINOR}/#v${MAJOR}-${MINOR}-${FIX}"

# Use appropriate API for your ticket system
GH_TOKEN=$(cat ~/.GITHUB_ACCESS_TOKEN) gh issue -R $GH_REPO create -a $MINION \
   -t "Review PaperCut $PRODUCT_UPCASE $INSTALLED_RELEASE upgrade to version $CURRENT_RELEASE" \
   -b "Review release notes at $RELEASE_NOTES"

echo -n $CURRENT_RELEASE > ~/LAST_VERSION_CHECKED
