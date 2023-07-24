FROM python:3.12.0b4-alpine

WORKDIR /usr/src/app 

COPY . ./
RUN pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT python rpc_server.py

EXPOSE 15672/tcp
EXPOSE 5672/tcp