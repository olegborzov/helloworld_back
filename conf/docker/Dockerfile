FROM docker.pkg.github.com/olegborzov/helloworld_back/hw_back_base:latest

# Copy all necessary files
COPY . /app/
WORKDIR /app/

# Install python requirements
RUN pip3 install --no-cache-dir -r requirements.txt
