FROM argus-common:latest

ENV CONTAINER_TYPE=presenter.curses

USER root
COPY . /app/argus/presenter/curses

USER appuser
RUN pip install --no-cache-dir \
    --no-warn-script-location \
    -r /app/argus/presenter/curses/requirements.txt && \
    pip freeze > /app/cache/python-packages-at-build.txt

CMD ["run", "presenter-curses"]
