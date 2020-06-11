FROM python:3.8-slim

# Copy all necessary files
COPY ./requirements.txt /app/
WORKDIR /app/

# Install debian packages, set timezone, install python packages, clear cache
RUN apt-get -y update \
  && apt-get -y upgrade \
  && apt-get install -qq -y --no-install-recommends \
      build-essential \
      gcc \
  && rm -rf /var/lib/apt/lists/*

# Install python requirements
RUN pip3 install -U pip && pip3 install --no-cache-dir -r requirements.txt
