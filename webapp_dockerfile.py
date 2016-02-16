webapp_dockerfile = """
FROM java
MAINTAINER di luo <di.luo@ele.me>
RUN mkdir /tomcat
ADD tomcat8 /tomcat

WORKDIR /tomcat/bin
RUN echo "now at"
RUN pwd
RUN ls
ENTRYPOINT ./startup.sh && tail -f ../logs/catalina.out
"""