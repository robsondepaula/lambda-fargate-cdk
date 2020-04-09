FROM python:3.7

# These environment variables will carry data from Lambda to Fargate
ENV LAMBDA_NAME = ""
ENV REQUEST_ID = ""

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

COPY task.py /src
CMD python /src/task.py