from python:3.11.3-slim-bullseye

RUN addgroup app --gid 10000 \
    && useradd app -d /opt -g app -s /bin/bash \
    && chown app:app /opt

USER app
WORKDIR /opt
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["./run.sh"]