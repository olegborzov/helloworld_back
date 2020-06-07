FROM python:3.8-slim

# Copy all necessary files
COPY ./requirements.txt /app/
WORKDIR /app/

# Install python requirements
RUN pip3 install -U pip && pip3 install --no-cache-dir -r requirements.txt
