#!/usr/bin/env python3

#  A trivial example of a custome user program for use with PaperCut NG or MF
#  See http://www.papercut.com/kb/Main/CaseStudyCustomUserSyncIntegration
#
#  Uses Python 3 to get access to arrays and be X platform.

import sys
import logging


userDatabase = [
    ["john","John Smith","johns@here.com","Accounts","Melbourne","1234"],
    ["jane","Jane Rodgers","jhanr@here.com","Sales","Docklands","5678"],
    ["ahmed","Ahmed Yakubb","ahmedy@here.com","Marketing","Home Office","4321"],
]


groupDatabase = [
    ["groupA","john"],
    ["groupB","ahmed","jane"],
    ]


logging.basicConfig(level=logging.DEBUG, filename="/tmp/logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

logging.info("Called with {}".format(sys.argv))


def getUser(userName):
   for user in userDatabase:
      if user[0] == userName:
         return user
   return ''


if len(sys.argv) < 2 or  sys.argv[1] != '-':
   print("incorrect argument passed {0}".format(sys.argv), file=sys.stderr)
   sys.exit(-1)

if sys.argv[2] == "is-valid":
   print('Y')
   sys.exit(0)
  
if sys.argv[2] == "all-users":
   for user in  userDatabase:
      print('/'.join(user))
   sys.exit(0)

if sys.argv[2] == "all-groups":
   for group in groupDatabase:
      print(group[0])
   sys.exit(0)


if sys.argv[2] == "get-user-details":
      name = input()
      u = getUser(name)
      if '' == u:
         print("Can't find user {0}".format(name), file=sys.stderr)
         sys.exit(-1)

      print('/'.join(u))
      sys.exit(0)

if sys.argv[2] == "group-member-names":
   for group in groupDatabase:
      if group[0] == sys-argv[3]:
         for user in group[1:]:
            print(user)
   sys.exit(0)


if sys.argv[2] == "group-members":
   for group in groupDatabase:
      if group[0] == sys.argv[3]:
         for user in group[1:]:
            print('/'.join(getuser(user)))
         sys.exit(0)
   print("Can't find gourp {}".format(sys.srgv[3]))
   sys.exit(-1)


   


print("Can't process arguments {0}".format(sys.argv), file=sys.stderr)
