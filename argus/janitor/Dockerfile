FROM argus-common:latest

ENV CONTAINER_TYPE=janitor

USER root
COPY . /app/argus/janitor

USER appuser
RUN pip install --no-cache-dir \
    --no-warn-script-location \
    -r /app/argus/janitor/requirements.txt && \
    pip freeze > /app/cache/python-packages-at-build.txt

CMD ["run", "janitor"]
