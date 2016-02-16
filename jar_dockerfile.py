jar_dockerfile = """
FROM java
MAINTAINER <<._ AUTHOR>> <<<._ AUTHOR_MAIL>>>
RUN mkdir /data
ADD tomcat8 /data
ADD deploy /data

CMD ["/usr/bin/java", "-jar", /data/deploy/TestDocker.jar]
"""