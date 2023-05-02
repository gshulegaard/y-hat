FROM ubuntu:22.04

RUN apt update && apt install -y python3-pip python3-setuptools python3-dev

# Install requirements for tests
COPY requirements.txt /opt/y-hat/requirements.txt
COPY requirements-dev.txt /opt/y-hat/requirements-dev.txt
RUN python3 -m pip install \
  -r /opt/y-hat/requirements.txt \
  -r /opt/y-hat/requirements-dev.txt

ENV PYTHONPATH /opt/y-hat

# This is mounted in the docker-compose file.
WORKDIR /opt/y-hat
ENTRYPOINT bash