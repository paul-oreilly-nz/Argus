If you are running Kafka on Aiven, please be aware that you will either need to set the planned topic up via the web UI in advance (recomended) or set 'kafka.auto_create_topics_enale' to True before you will be able to push events into Kafka.

(Events need a home, and you need to make it or let the scripts make it for you, but either way needs some action in advance)
