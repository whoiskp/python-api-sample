FROM python:3.6-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /whoiskp
WORKDIR /whoiskp

EXPOSE 5000
