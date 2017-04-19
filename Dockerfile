FROM alpine:3.3
RUN apk add --update python python-dev py-pip bash 
RUN pip install --upgrade pip && pip install virtualenv && rm -rf /var/cache/apk/*

WORKDIR /app

COPY *.py /app/
COPY requirements.txt /app/
COPY *.db /app/
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

EXPOSE 8000
ENTRYPOINT ["/env/bin/python","main.py"]
