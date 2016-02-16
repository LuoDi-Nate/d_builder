jar_dockerfile = """
FROM java
MAINTAINER <<._ AUTHOR>> <<<._ AUTHOR_MAIL>>>
RUN mkdir /deploy
ADD firstblood /deploy

RUN chmod 777 /deploy/start.sh

RUN mkdir -p /data/logs

RUN chmod 777 /data/logs

CMD ["nohup","/deploy/start.sh","&"]
"""