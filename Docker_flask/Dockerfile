
FROM python:3.8
# define the present working directory
WORKDIR /Docker_flask
# copy the contents into the working dir
ADD . /Docker_flask
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container
CMD ["python","app.py"]