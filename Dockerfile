FROM python:3.11

RUN mkdir /backend

WORKDIR /backend

RUN pip install gunicorn
RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install

RUN chmod a+x docker/*.sh
