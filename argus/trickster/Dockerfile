FROM argus-common:latest

ENV CONTAINER_TYPE=trickster

USER root
COPY . /app/argus/trickster

USER appuser
RUN pip install --no-cache-dir \
    --no-warn-script-location \
    -r /app/argus/trickster/requirements.txt && \
    pip freeze > /app/cache/python-packages-at-build.txt

CMD ["run", "trickster"]
