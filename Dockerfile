FROM snakepacker/python:all as builder

RUN python3.8 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/app/bin/pip install -Ur /mnt/requirements.txt

COPY . /mnt/dist/
RUN /usr/share/python3/app/bin/pip install /mnt/dist/

FROM snakepacker/python:3.8 as api

COPY --from=builder /usr/share/python3/app /usr/share/python3/app

EXPOSE 8080

RUN ln -snf /usr/share/python3/app/bin/analyzer-* /usr/local/bin/

CMD ["enrollment"]