FROM python:3.8 as build

RUN pip install -U pip

RUN mkdir /usr/src/enrollment
COPY . /usr/src/enrollment

WORKDIR /usr/src/enrollment

EXPOSE 8080

RUN pip install .

RUN ln -snf /usr/share/python3/app/bin/enrollment* C:\Users\Я\Desktop

CMD ["enrollment", "postgresql+asyncpg://admin:admin@pg/maindb"]