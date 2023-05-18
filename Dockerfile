from python:3.11.3-alpine3.18

WORKDIR /opt
COPY . .
RUN apk update && apk add gcc g++ musl-dev linux-headers cmake
RUN pip3 install -r requirements.txt
CMD ["gunicorn","--reload","--access-logfile","'-'","'app:http()'"]

