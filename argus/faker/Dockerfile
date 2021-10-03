FROM argus-common:latest

ENV CONTAINER_TYPE=faker

USER root
COPY . /app/argus/faker

USER appuser
RUN pip install --no-cache-dir \
    --no-warn-script-location \
    -r /app/argus/faker/requirements.txt && \
    pip freeze > /app/cache/python-packages-at-build.txt

CMD ["run", "faker"]
