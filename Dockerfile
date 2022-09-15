FROM python:3.8 as build

RUN pip install -U pip

RUN mkdir /usr/src/enrollment
COPY . /usr/src/enrollment

WORKDIR /usr/src/enrollment

EXPOSE 8080

RUN pip install .

CMD ["enrollment"]