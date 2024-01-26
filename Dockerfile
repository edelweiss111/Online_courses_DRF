FROM python:3

WORKDIR /Online_courses_DRF

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
