FROM python:3.9.1

WORKDIR /opt/kuptelefonik

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e /opt/kuptelefonik/data_scraping

