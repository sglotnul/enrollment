FROM python:3.8 as build

RUN pip install -U pip

RUN mkdir /usr/src/app
COPY . /usr/src/app

WORKDIR /usr/src/app

EXPOSE 8080
EXPOSE 5432

RUN pip install .

CMD ["enrollment"]