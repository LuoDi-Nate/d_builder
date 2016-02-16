jar_dockerfile = """
FROM java
MAINTAINER di luo <di.luo@ele.me>
RUN mkdir /data
ADD tomcat8 /data
ADD deploy /data
EXPOSE 8080

CMD ["/usr/bin/java", "-jar", /data/deploy/TestDocker.jar]
"""