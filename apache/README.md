# apache

Thsi folder contains a Docker compose script to run a local copy of Apache web server which can then be used to test all the redirects with using the run-tests.py script.

Run `docker compose -f docker-compose.yml up -d` to run Apache and then just `python run-tests.py`.

Stop Apache with `docker compose -f docker-compose.yml down`.
