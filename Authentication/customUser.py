#!/usr/bin/env python3


#  A trivial example of a custom user program for use with PaperCut NG or MF
#  See http://www.papercut.com/kb/Main/CaseStudyCustomUserSyncIntegration
#
#  Uses Python 3 for dictionaries and be X platform. Make sure that the
#  Python interpreter is on the path for the PaperCut service account or specify
#  the path explicitly.

#  N.B. This example is for illustrative purposes only. Any production solution
#  needs to be optimised for performance.

import sys
import logging
import xmlrpc.client
from ssl import create_default_context, Purpose

auth="token"
host="https://localhost:9192/rpc/api/xmlrpc"

userDatabase = {
    "john": {"fullname":"John Smith",   "email":"johns@here.com",  "dept":"Accounts",  "office":"Melbourne",   "cardno":"1234", "otherEmails":"personal1@webmail.com", "secondarycardno":"01234","password":"password1"},
    "jane": {"fullname":"Jane Rodgers", "email":"janer@here.com",  "dept":"Sales",     "office":"Docklands",   "cardno":"5678", "otherEmails":"personal2@webmail.com", "secondarycardno":"05678", "password":"password2"},
    "ahmed":{"fullname":"Ahmed Yakubb", "email":"ahmedy@here.com", "dept":"Marketing", "office":"Home Office", "cardno":"4321", "otherEmails":"personal3@webmail.com", "secondarycardno":"04321", "password":"password3"},
}

groupDatabase = {
    "groupA":["john"],
    "groupB":["ahmed", "jane"],
}

# logging.basicConfig(level=logging.DEBUG, filename="/tmp/logfile", filemode="a+",
#                         format="%(asctime)-15s %(levelname)-8s %(message)s")

# logging.info("Called with {}".format(sys.argv))


def formatUserDetails(userName):
    if userName in userDatabase:
        if extraData:
            return '\t'.join([userName, userDatabase[userName]["fullname"], userDatabase[userName]["email"], userDatabase[userName]["dept"], userDatabase[userName]["office"],
                                        userDatabase[userName]["cardno"], userDatabase[userName]["otherEmails"], userDatabase[userName]["secondarycardno"]])
        else:
            return '\t'.join([userName, userDatabase[userName]["fullname"], userDatabase[userName]["email"], userDatabase[userName]["dept"], userDatabase[userName]["office"]])
    else:
        print("Call to formatUserDetails error for username {}".format(userName), file=sys.stderr)
        sys.exit(-1)

# Should be return short or long form user data? Let's ask PaperCut MF/NG
proxy = xmlrpc.client.ServerProxy(host, verbose=False, 
                context = create_default_context(Purpose.CLIENT_AUTH))

try:
    extraData = "N" != proxy.api.getConfigValue(auth, "user-source.update-user-details-card-id")
except Exception:
    print("Cannot use web services API. Please configure", file=sys.stderr)
    sys.exit(-1)

# Being called as user auth program
if len(sys.argv) == 1:
    name = input()
    password = input()
    if name in userDatabase and userDatabase[name]["password"] == password:
        print("OK\n{}\n".format(name)) # Note: return canonical user name
        sys.exit(0)
    else:
        print("Wrong username or password", file=sys.stderr)
        print("ERROR\n")
        sys.exit(-1)

if len(sys.argv) < 2 or  sys.argv[1] != '-':
    print("incorrect argument passed {0}".format(sys.argv), file=sys.stderr)
    sys.exit(-1)

# Being called as user sync program
if sys.argv[2] == "is-valid":
    print('Y')
    print("long form user data record will provided" if extraData else "short form user data record will provided")
    sys.exit(0)

if sys.argv[2] == "all-users":
    for name in userDatabase:
        print(formatUserDetails(name))
    sys.exit(0)

if sys.argv[2] == "all-groups":
    print('\n'.join([g for g in groupDatabase]))
    sys.exit(0)

if sys.argv[2] == "get-user-details":
    name = input()
    if name in userDatabase:
        print(formatUserDetails(name))
        sys.exit(0)
    else:
        print("Can't find user {0}".format(name), file=sys.stderr)
        sys.exit(-1)

if sys.argv[2] == "group-member-names":
    if sys.argv[3] in groupDatabase:
        for user in groupDatabase[sys.argv[3]]:
            if user in userDatabase:
                print(user)
            else:
                print("Invalid user name {} found in group list {}".format(user, group), file=sys.stderr)
                sys.exit(-1)
        sys.exit(0)
    else:
        print("Group name {} not found".format(sys.argv[3]), file=sys.stderr)
        sys.exit(-1)

if sys.argv[2] == "group-members":
    if sys.argv[3] in groupDatabase:
        for user in groupDatabase[sys.argv[3]]:
            if user in userDatabase:
                print(formatUserDetails(user))
            else:
                print("Invalid user name {} found in group list {}".format(user, group), file=sys.stderr)
                sys.exit(-1)
        sys.exit(0)
    else:
        print("Group name {} not found".format(sys.argv[3]), file=sys.stderr)
        sys.exit(-1)

if sys.argv[2] == "is-user-in-group":
    if sys.argv[3] in groupDatabase:
        if sys.argv[4] in groupDatabase[sys.argv[3]]:
            print('Y')
            sys.exit(0)
        print('N')
        sys.exit(0)
    print("Invalid Group name {}".format(sys.argv[3]), file=sys.stderr)
    sys.exit(-1)

print("Can't process arguments {0}".format(sys.argv), file=sys.stderr)
