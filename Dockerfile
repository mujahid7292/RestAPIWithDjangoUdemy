# Bring Base Image From The Docker Hub
FROM python:3.7-alpine

# Name Of The Code Maintainer & Email 
MAINTAINER Saifullah al Mujahid <mujahid7292@gmail.com>

# Let set python unbuffered environment variable.
ENV PYTHONUNBUFFERED 1
# What this environment variable does, is that it tell python
# to run in unbuffered mode. This is recommended when running 
# python inside docker container. The reason for this, is that 
# it does not allow python to buffer the output. So it reduce
# the error in running python inside docker image.

# We are going to store our projects dependencies in the
# ./requirements.txt file.
COPY ./requirements.txt  /requirements.txt
# This command will copy this file to inside the docker image
# in the following '/' directory.

# Now we will install all of the dependencies of our project.
RUN pip install -r /requirements.txt

# We will create a directory(/app) within our docker image, that we can use
# to store our application source code.
RUN mkdir /app
# Create a directory/folder named 'app' inside our docker image
WORKDIR /app
# Switched to this 'app' directory as a default directory.
# Any application that we run inside our docker container, will start
# running from this location.
COPY ./app /app
# Copy all the source code from our local machine './app' folder to the directory
# inside docker container which is also '/app' folder.

# We will create an user who will run our application using docker.
RUN adduser -D mujahid7292
# -D = Create an user without admin privilage. That means this user will only be able 
# to run this docker image & will not get any root access.
# mujahid7292 = Name of the user.
USER mujahid7292
# Now docker will switched to this 'mujahid7292' user.