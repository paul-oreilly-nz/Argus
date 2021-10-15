Argus
=====

Keeping an eye on things.


Requirements
============

Argus has been built with a docker basis. To run any of the components, you will need
to have docker installed. A 'docker-compose.yml' has also been provided for ease of 
use, and installing docker-compose is a quick method to get started.

Instructions for installing docker can be found here:
https://docs.docker.com/get-docker/

Instructions for installing docker-compose can be found here:
https://docs.docker.com/compose/install/



Components
==========

Faker
Currently the only data source, Faker generates false records of CPU data (load and time data) for testing.

Caterpillar
Digests the data stream from Kafka and transforms it into structured data inside of Postgres

Terminal Monitor
A very simple monitor that runs inside of a terminal to montior one data source and show the latest record of activity



Security
========

Secrets are managed by both environmental variables (via including .env files in the docker-compose.yml) and referencing files added to the container at run time via mounts.



Logs
====

Following docker's best practice, containers are a single thread / item only, and by default are set to log to stdout. The roadmap does include more diverse options for the future.



Planned Additions
=================

End to End Testing
Generate sets of fake data, send via Kafka, consume as pr normal into Postgres, and verify 
from Postgres that the data has correctly passed through the entire chain.

Reporter
Using pyutil, the next item on the roadmap is to monitor real CPU's rather than pretend ones

Tricker
Expanding on Faker, a system that sends malformed data to try and corrupt or break the system during testing

Janitor
The one that cleans out the older Postgres database enteries, based on how old they are.

Curses-UI
To watch multiple systems at once

Additional data types
Adding filesystems, network information, etc to the items being monitored
