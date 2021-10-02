FROM argus-common:latest

ENV CONTAINER_TYPE=reporter

USER root
COPY . /app/argus/reporter

USER appuser
RUN pip install --no-cache-dir \
    --no-warn-script-location \
    -r /app/argus/reporter/requirements.txt && \
    pip freeze > /app/cache/python-packages-at-build.txt

CMD ["run", "reporter"]
