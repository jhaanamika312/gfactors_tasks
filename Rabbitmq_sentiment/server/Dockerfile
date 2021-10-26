# init a base image
FROM python:3.8

#define present working directory
WORKDIR /server

#Copy contents into working dir
ADD . /server

#Install dependencies 
RUN pip install -r requirements.txt

#command to build the image
CMD ["python", "app.py"]

