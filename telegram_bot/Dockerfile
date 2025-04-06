FROM python:3.12
LABEL authors="MatMex-Week"

# Update packages
RUN apt-get update && apt-get upgrade -y

# Set enviroment variables
ENV TZ Europe/Moscow
ENV PIP_ROOT_USER_ACTION=ignore

# Prepare project directory
CMD mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

# Copy and install requirements
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project to directory
COPY . ./

# Run api
ENTRYPOINT python3 run.py
