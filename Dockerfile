# Stable python3
FROM python:3

# Arguments
ARG user=main
ARG group=main
ARG uid=1004
ARG gid=1005

# Whos your daddy
LABEL MAINTAINER="Idelfrides Jorge <eng.idelfridesjorge@gmail.com>"

# Prepare directiories
RUN mkdir -p /StarkBankChallengeFlask/stage
RUN mkdir -p /StarkBankChallengeFlask/stage/SB_SDK_KEYS
RUN mkdir -p /StarkBankChallengeFlask/stage/OUTPUT_FILES
RUN mkdir -p /StarkBankChallengeFlask/stage/FILES_DIR

# Define workdir
WORKDIR /StarkBankChallengeFlask

# Copy files
ADD . /StarkBankChallengeFlask

# My projects home directory is a volume, so configuration and build history
# can be persisted and survive image upgrades
VOLUME /StarkBankChallengeFlask/stage

# Install gcc
RUN apt-get update && apt-get install -y \
        wget \
	curl \
	gnupg \
        gcc \
        g++ \
        unixodbc-dev \
        unrar

RUN apt-get update

# upgrade pip
RUN pip install --upgrade pip

# Get plugins
RUN pip install -r requirements.txt
RUN pip install tornado

# Clean
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
	&& rm -rf /var/lib/apt/lists/*

# Turn executable
RUN chmod +x /StarkBankChallengeFlask/cmd_docker.sh

# Define ports
EXPOSE 7007
EXPOSE 7000

# Define user
USER main


RUN echo "snap install ngrok"
RUN echo "ngrok config add-authtoken CIzE7FJEeaEDh0ASL4GqUrpCtl_5j2UAEh18VnNNZzpNNoCG"
RUN echo "ngrok config add-api_key ak_2CJOZXfRZdJOZABSJo6g9wXcF9o"
RUN echo "ngrok http 7007"


# Execute server
CMD ["/StarkBankChallengeFlask/cmd_docker.sh"]
