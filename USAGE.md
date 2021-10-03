Building the Containers
=======================

With docker installed, running the build script will build each of the required containers:
'build-all.sh'

Having done so, you can verify what images are ready by running 'docker images ls'



Environment files and Secrets
=============================

At present the docker-compose.yml makes use of .env files and a secrets folder that is mounted inside of the container. Examples have been provided, but will need to be updated with a set of working credentials before use.



Generating Fresh Data
=====================

From the same folder as the 'docker-compose.yml', and after doing the above, running 'docker-compose up' will run both the Faker and Catepillar for a minute to generate fresh data



Watching for Fresh Data
=======================


Running the terminal monitor script, providing the name of the 'provider' that you want to watch as the first arguement, will keep a real time eye on the last record in the Postgres database for that stream.
