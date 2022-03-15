FROM grpc/python

WORKDIR .

#RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt

RUN apt-get -y update
RUN apt install -y software-properties-common
RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu main universe restricted multiverse"
#RUN add-apt-repository universe

RUN apt-get -y install python3-pip
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install --upgrade protobuf

EXPOSE 5001

COPY . .
CMD ["python3", "server.py"]