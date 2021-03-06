FROM python:3.6

WORKDIR /opt/

COPY . .

RUN python3.6 -m pip install -r requirements.txt


EXPOSE 8080

