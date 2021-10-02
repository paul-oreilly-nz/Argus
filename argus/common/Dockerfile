FROM python:3.9.7-bullseye

# Make a non root user for running the code inside the containers
RUN groupadd -g 999 appuser && \
    useradd -m -r -u 999 -g appuser appuser

# A folder inside the container to hold the application code and configs
WORKDIR /app/argus

# Create an area that the apps can save data to (and an easy storage volume for persistant operation)
RUN mkdir -p /app/cache && \
    chown appuser:appuser /app/cache

# copy over the common files (with root permission, therefore read-only to running processes)
COPY . /app/argus/common

# switch to our non-root user to install packages locally with pip
USER appuser
RUN pip install --no-cache-dir --no-warn-script-location -r /app/argus/common/requirements.txt

ENTRYPOINT ["/app/argus/common/entrypoint.py"]
