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

# Temp Workaround for DNS issue
RUN echo http://nl.alpinelinux.org/alpine/v3.9/main > /etc/apk/repositories; \
    echo http://nl.alpinelinux.org/alpine/v3.9/community >> /etc/apk/repositories
    
# We are going to store our projects dependencies in the
# ./requirements.txt file.
COPY ./requirements.txt  /requirements.txt
# This command will copy this file to inside the docker image
# in the following '/' directory.

# To install 'psycopg2' package from our 'requirements.txt'
# file, first we need to install 'postgresql-client'.
RUN apk add --update --no-cache postgresql-client
# This above run command will use the package manager
# that comes from python:3.7-alpine (which is apk)
# and we are going to add a package (by add command)
# and this '--update' command means update the registry
# before adding the package.
# --no-cache = means, don't store the registry index
# on our Dockerfile. The reason we do this, is because
# we really want to minimize number of extra files &
# packages that are included in our docker container.
# This is best practice, because it means that your
# docker container for your application has the smallest 
# footprint possible. And it also means, you don't include
# any extra dependencies on your system, which may cause
# sequrity vulnerabilities in your system.

# Now we are going to install some temporary packages
# that need to be installed on the system, while we run
# our requirements.txt file, then we can remove them
# after installing all of the package from requirements.txt
# file.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
# --virtual = it help us to easilly remove those dependencies
# later. So here it is called '.tmp-build-deps' or temporary
# build dependencies.
# \ = means, go to next line.

# Now we will install all of the dependencies of our project.
RUN pip install -r /requirements.txt

# After installing all the dependecies / package from
# requirements.txt file, we will delete all our temporary
# build dependencies / packages
RUN apk del .tmp-build-deps

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