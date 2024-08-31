FROM python:3.12-slim

ENV PIP_NO_CACHE_DIR=TRUE
ENV PIP_DISABLE_PIP_VERSION_CHECK=TRUE

RUN mkdir -p /opt/program
WORKDIR /opt/program

COPY requirements.txt /opt/program/
RUN python3 -m pip install -r /opt/program/requirements.txt
COPY src/job /opt/program/job

EXPOSE 8080

CMD ["python3","job/export.py"]