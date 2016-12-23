# our base image
FROM ubuntu:latest

# Install python and pip
RUN apt-get update -y
RUN apt-get install -y python-pip libssl-dev libxml2-dev libxslt1-dev \
libffi-dev libncurses5-dev

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN touch __init__.py
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY scrapy.cfg /usr/src/app/
COPY app/ /usr/src/app/
COPY templates/index.html /usr/src/app/templates/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "/usr/src/app/app.py"]
