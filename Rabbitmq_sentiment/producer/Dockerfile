
FROM python:3.8


RUN pip install pika



WORKDIR /usr/src/app

COPY publisher.py .


CMD ["python", "/usr/src/app/publisher.py"]