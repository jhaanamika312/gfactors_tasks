
FROM python:3.10

RUN pip install pika


# Actually install the application
WORKDIR /usr/src/app

COPY worker.py .

CMD ["python", "/usr/src/app/worker.py"]