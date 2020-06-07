FROM hw_base

# Copy all necessary files
COPY . /app/
WORKDIR /app/

# Install python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Create dir for celery files
RUN mkdir /tmp/celery/
