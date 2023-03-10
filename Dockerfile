FROM python:3.9.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend
COPY requirements.txt /backend/

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y python3 pip

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /backend

EXPOSE 8000

CMD uvicorn --host=0.0.0.0 --port 8000 main:app