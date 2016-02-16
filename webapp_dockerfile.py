webapp_dockerfile = """
FROM java
MAINTAINER <<._ AUTHOR>> <<<._ AUTHOR_MAIL>>>
RUN mkdir /tomcat
ADD tomcat8 /tomcat

WORKDIR /tomcat/bin
RUN echo "now at"
RUN pwd
RUN ls
ENTRYPOINT ./startup.sh && tail -f ../logs/catalina.out
"""