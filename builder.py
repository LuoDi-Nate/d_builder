import getopt
import sys
import os

import jar_dockerfile as jar
import webapp_dockerfile as war


print 'builder start ...'

# def args, only enum in ("jar", "war", "html")
app_type = "jar"

app_path = "~/"

app_bind = {}

app_server_name = ""

app_version = "0.0"

app_author = "nobody"

app_author_mail = "nobody@sample.com"


def exit_with_msg(msg):
    print msg
    exit(1)

# args resolver
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

        # like "80:8080#443:8443"
        if value:
            bind_list = value.split('#')

            for bind in bind_list:
                host_port, virtual_port = bind.split(":")
                app_bind[host_port] = virtual_port

        print app_bind

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


# check necessary
def check_args_4_jar():
    if not app_path:
        exit_with_msg("no path for deploy apps.")
    if not app_bind:
        print("[warn]   this jar app has no port binding.")
    if not app_server_name:
        exit_with_msg("no app name is invalid.")
    if app_version == "0.0":
        print("[warn]   no version set, use default 0.0")


def check_args_4_webapp():
    if not app_path:
        exit_with_msg("no path for deploy apps.")
    if not app_bind:
        exit_with_msg("webapp need last 1 port binding.")
    if not app_server_name:
        exit_with_msg("no app name is invalid.")
    if app_version == "0.0":
        print("[warn]   no version set, use default 0.0")


def check_args_4_html():
    pass

# check app_type validation
if app_type not in ("war", "jar", "html"):
    exit_with_msg("unknown app type for %s" % app_type)


# replace dockerfile
def replace_args_4_jar():
    jar.jar_dockerfile.replace("<<._ AUTHOR>>", app_author)
    jar.jar_dockerfile.replace("<<._ AUTHOR_MAIL>>", app_author_mail)


def replace_args_4_war():
    war.webapp_dockerfile.replace("<<._ AUTHOR>>", app_author)
    war.webapp_dockerfile.replace("<<._ AUTHOR_MAIL>>", app_author_mail)


def replace_args_4_html():
    pass

# check args with app type
if app_type == "war":
    check_args_4_webapp()
    replace_args_4_war()

elif app_type == "jar":
    check_args_4_jar()
    replace_args_4_jar()

elif app_type == "html":
    check_args_4_html()
    replace_args_4_html()