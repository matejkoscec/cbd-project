#!/bin/bash

CONTAINER_NAME=spark
export DOCKER_CLI_HINTS=false

if ! docker compose -f "docker-compose.yaml" ps -q | grep -q .; then
  echo "Docker compose not running, starting..."
  echo "Starting compose"
  docker compose up -d
  printf "\nRunning startup script\n"
  docker exec -it $CONTAINER_NAME /bin/bash -c "/startup.sh --init"
  printf "\e[32m\n> Startup done\e[0m\n"

  if [ "$1" == "--interactive" ] || [ "$1" == "-i" ]; then
    printf "\nInteractive mode\n"
    echo "If you want to run jobs manually, run the 'project/analysis.sh' script."
    docker exec -it $CONTAINER_NAME /bin/bash
  else
    printf "\nRunning the data analysis\n"
    docker exec $CONTAINER_NAME /bin/bash -c "project/analysis.sh"
    printf "\e[32m\n> Done\e[0m\n"
  fi

  echo "Getting misc files"
  source get_output.sh
  exit 0
fi

echo "Docker compose running, updating files"
docker exec -it $CONTAINER_NAME /bin/bash -c "/startup.sh"

if [ "$1" == "--interactive" ] || [ "$1" == "-i" ]; then
  printf "\nInteractive mode\n"
  echo "If you want to run jobs manually, run the 'project/analysis.sh' script."
  docker exec -it $CONTAINER_NAME /bin/bash
else
  printf "\nRunning the data analysis\n"
  docker exec $CONTAINER_NAME /bin/bash -c "project/analysis.sh"
  printf "\e[32m\n> Done\e[0m\n"
fi

rm -rf misc/*
echo "Getting misc files"
source get_output.sh