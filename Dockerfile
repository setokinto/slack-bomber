FROM python:3.9.0
MAINTAINER Kouki Saito <dan.addr.skd@gmail.com>

RUN groupadd -r slackbot && useradd -r -g slackbot slackbot
COPY . /app
WORKDIR /app
RUN python setup.py develop

USER slackbot
CMD ["python", "main.py"]

