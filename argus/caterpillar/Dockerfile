FROM argus-common:latest

ENV CONTAINER_TYPE=caterpillar

USER root
COPY . /app/argus/caterpillar

USER appuser
RUN pip install --no-cache-dir \
    --no-warn-script-location \
    -r /app/argus/caterpillar/requirements.txt && \
    pip freeze > /app/cache/python-packages-at-build.txt

CMD ["run", "caterpillar"]
