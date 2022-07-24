# Stable python3
FROM python:3

# Whos your daddy
LABEL MAINTAINER="Idelfrides Jorge <eng.idelfridesjorge@gmail.com>"

# Define workdir
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements-dev.txt ./

# Copy files
ADD . /usr/src/app/

COPY . .

# Prepare directiories | IJ
RUN mkdir -p /starkbankchallenge_flask/stage
RUN mkdir -p /starkbankchallenge_flask/stage/SB_SDK_KEYS
RUN mkdir -p /starkbankchallenge_flask/stage/OUTPUT_FILES
RUN mkdir -p /starkbankchallenge_flask/stage/FILES_DIR


# My projects home directory is a volume, so configuration and build history
# can be persisted and survive image upgrades
VOLUME /starkbankchallenge_flask/stage

# Install gcc
RUN apt-get update && apt-get install -y wget curl gnupg gcc g++ unixodbc-dev

RUN apt-get update

# upgrade pip
RUN pip install --upgrade pip

RUN pip3 install virtualenv

# Get plugins
RUN pip install --no-cache-dir  -r requirements.txt

# Define ports
EXPOSE 7000


# Execute server
CMD [ "python", "./flask_starkbank_app.py" ]
