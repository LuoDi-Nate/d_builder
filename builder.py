import getopt
import sys
import os

print 'builder start ...'

app_type = "jar"

app_path = "~/"

app_bind = ""

app_server_name = ""

app_version = "0.0"


def exit_with_msg(msg):
    print msg
    exit(1)

try:
    opts, args = getopt.getopt(sys.argv[1:], "t:u:p:n:v:")

for opt, value in opts:
    if opt == '-t':
        print "-t :", value
        if value not in ("jar", "war"):
            exit_with_msg("invalid value : \'-t\' :" + value)

        app_type = value

    elif opt == '-u':
        print "-u :", value
        if not os.path.exists(value):
            exit_with_msg("invalid value : \'-p\' :" + value)

        app_path = value

    elif opt == '-p':
        print '-p', value

        app_bind = value

    elif opt == '-n':
        print '-n :', value

        if not value:
            exit_with_msg("invalid value  \'-n\'" + value)

        app_server_name = value

    elif opt == '-v':
        print '-v :', value
        if not value:
            exit_with_msg("invalid value  \'-v\'" + value)

        app_version = value

    else:
        exit_with_msg("unknown arg:" + opt)
