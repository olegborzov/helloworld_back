FROM hw_base

# Copy all necessary files
COPY . /app/
WORKDIR /app/

# Install python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Run server
EXPOSE 5000
CMD [ "uwsgi", "--http", ":5000", \
               "--chown", "www-data:www-data", \
               "--uid", "www-data", \
               "--gid", "www-data", \
               "--processes", "4", \
               "--threads", "2", \
               "--wsgi", "run_server:app" ]
