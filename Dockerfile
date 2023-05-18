from python:3.11.3-slim-bullseye

WORKDIR /opt
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["./run.sh"]