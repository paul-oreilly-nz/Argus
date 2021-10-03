FROM argus-common:latest

ENV CONTAINER_TYPE=presenter-terminal

USER root
COPY requirements.txt /app/argus/presenter-terminal/

USER appuser
RUN pip install --no-cache-dir \
    --no-warn-script-location \
    -r /app/argus/presenter-terminal/requirements.txt && \
    pip freeze > /app/cache/python-packages-at-build.txt

USER root
COPY . /app/argus/presenter-terminal

USER appuser

ENTRYPOINT ["/usr/bin/env", "python3", "/app/argus/presenter-terminal/TerminalMonitor.py"]

