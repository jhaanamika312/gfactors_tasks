FROM python:3.8

#define present working directory
WORKDIR /worker

#Copy contents into working dir
ADD . /worker

#Install dependencies 
RUN pip install -r requirements.txt

#define command to build the image
CMD ["python", "worker.py"]