import getopt
import sys
import os
import time

import jar_dockerfile as jar
import webapp_dockerfile as war


"""
config 4 builder
"""
setup_path = "/tmp/data3/docker_file/"

tomcat_path = "/tmp/data3/tomcat8"


print 'builder start ...'

# def args, only enum in ("jar", "war", "html")
app_type = "jar"

app_path = "~/"

app_bind = {}

app_server_name = ""

app_version = "0.0"

app_author = "nobody"

app_author_mail = "nobody@sample.com"

jar_docker_file = ""

war_docker_file = ""

html_docker_file = ""


def exit_with_msg(msg):
    print msg
    exit(1)

# args resolver
opts, args = getopt.getopt(sys.argv[1:], "t:u:p:n:v:a:m:")

for opt, value in opts:
    if opt == '-t':
        print "-t :", value
        if value not in ("jar", "war"):
            exit_with_msg("invalid value : \'-t\' :" + value)

        app_type = value

    elif opt == '-u':
        print "-u :", value
        if not os.path.exists(value):
            exit_with_msg("file not found : \'-u\' :" + value)

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

    elif opt == '-a':
        print '-a', value
        if not value:
            exit_with_msg("invalid value \'-a\'" + value)

        app_author = value

    elif opt == '-m':
        print '-m', value
        if not value:
            exit_with_msg("invalid value \'-m\'" + value)

        app_author_mail = value

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
    print "make docker file 4 jar"
    global jar_docker_file, app_author, app_author_mail
    jar_docker_file = jar_docker_file.replace("<<._ AUTHOR>>", app_author)
    jar_docker_file = jar_docker_file.replace("<<._ AUTHOR_MAIL>>", app_author_mail)


def replace_args_4_war():
    print "make docker file 4 war"
    global war_docker_file, app_author, app_author_mail
    war_docker_file = war_docker_file.replace("<<._ AUTHOR>>", app_author)
    war_docker_file = war_docker_file.replace("<<._ AUTHOR_MAIL>>", app_author_mail)


def replace_args_4_html():
    print "make docker file 4 html"
    pass


# exec shell with this func, if result not 0 , exit with cmd
def exec_cmd_via_shell_result_true(cmd):
    print "exec shell : [%s]" % cmd
    result = os.system(cmd)
    # in linux , 0 is true, any else will be regarded error
    if result:
        exit_with_msg("error during exec this :[%s]" % cmd)
    print "done."

# check args with app type
if app_type == "war":
    check_args_4_webapp()
    war_docker_file = war.webapp_dockerfile
    replace_args_4_war()

elif app_type == "jar":
    check_args_4_jar()
    jar_docker_file = jar.jar_dockerfile
    replace_args_4_jar()


elif app_type == "html":
    check_args_4_html()
    # TODO make html docker file
    replace_args_4_html()

# generator dir name 4 dockerfile
time_str = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
print "time now:%s" % time_str

dir_name = "%s%s_%s_%s_%s" % (setup_path, time_str, app_type, app_server_name, app_version)
print "making working dir... [%s]" % dir_name

cmd = "mkdir -p %s" % dir_name
exec_cmd_via_shell_result_true(cmd)

# move app to setup path
# cmd = "cp -r %s %s" % (app_path, dir_name)
# exec_cmd_via_shell_result_true(cmd)


# generator docker file
dockerfile_path = "%s/%s" % (dir_name, "Dockerfile")


def gen_dockerfile_by_apptype(app_type, dockerfile_path):
    #create file
    print "touch Dockerfile..."
    cmd = "touch %s" % dockerfile_path
    exec_cmd_via_shell_result_true(cmd)

    file = open(dockerfile_path, "w")

    print "generator docker file..."
    if app_type == "jar":
        file.write(jar_docker_file)
    elif app_type == "war":
        file.write(war_docker_file)
    elif app_type == "html":
        pass
    else:
        exit_with_msg("wrong app type.")

    file.flush()
    file.close()

# gen
gen_dockerfile_by_apptype(app_type, dockerfile_path)


# jar build operation
def build_jar():
    cmd = "mkdir -p %s/firstblood" % dir_name
    exec_cmd_via_shell_result_true(cmd)

    # unzip zipfile to deploy
    cmd = "unzip %s/%s.zip -d %s/firstblood" % (app_path, app_server_name, dir_name)
    exec_cmd_via_shell_result_true(cmd)

    cmd = "cp %s/start.sh %s/firstblood/start.sh" % (app_path, dir_name)
    exec_cmd_via_shell_result_true(cmd)

    print "build done! exec downstairs shell ..."
    cmd = "cd %s ; sudo docker build -t \"%s-%s-%s\" . " % (dir_name, app_type, app_version, app_server_name)

    exec_cmd_via_shell_result_true(cmd)

    print "sudo docker run -d --name=\'%s\' ${container_hash}" % { app_server_name}


# war build operation
def build_war():
    # copy tomcat here
    cmd = "cp -r %s %s" % (tomcat_path, dir_name)
    exec_cmd_via_shell_result_true(cmd)

    # deploy
    cmd = "rm -rf %s/tomcat8/webapps/ROOT/*" % (dir_name)
    exec_cmd_via_shell_result_true(cmd)

    cmd = "unzip %s/%s.war -d %s/tomcat8/webapps/ROOT" % (app_path, app_server_name, dir_name)
    exec_cmd_via_shell_result_true(cmd)

    print "build done! exec downstairs shell ..."
    cmd = "cd %s ; sudo docker build -t \"%s-%s-%s\" . " % (dir_name, app_type, app_server_name, app_version)
    exec_cmd_via_shell_result_true(cmd)

    print "docker image built done, get container hash code up ^ , and run command down ;"

    port_binding = ""

    for physical, virtual in app_bind:
        port_binding += " -p "
        port_binding += physical + ":" + virtual

    print "sudo docker run -d %s --name=\'%s\' ${container_hash}" % {port_binding, app_server_name}

# begin build
print "begin build..."

if app_type == "jar":
    build_jar()
elif app_type == "war":
    build_war()
elif app_type == "html":
    pass



