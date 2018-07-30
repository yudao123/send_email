FROM ubuntu:16.04

WORKDIR /opt/send_email

COPY send_email.py /opt/send_email

RUN sed -i -s 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y \
  python python-pip

RUN pip install -U \
    pip \
    pyzmail==1.0.3
