###To launch docker-compose in dev:
docker-compose -f "docker-compose-dev.yml" up -d --build

###To launch prod:
docker-compose up

###To build docker image locally:
docker build --pull --rm -f "Dockerfile" -t dopamine:latest "."
