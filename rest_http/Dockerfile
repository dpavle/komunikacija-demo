FROM python:3.12.0b4-alpine

WORKDIR /usr/src/app 

COPY . ./
RUN pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT python server.py

EXPOSE 5000/tcp
