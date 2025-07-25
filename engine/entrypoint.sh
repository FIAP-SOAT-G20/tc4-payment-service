#!/usr/bin/env bash

# shellcheck disable=SC2164
cd /engine

if [[ -z "${HOST}" ]]; then
  export HOST=0.0.0.0
fi

echo "Configuring listener on: $HOST"

if [[ -z "${PORT}" ]]; then
  export PORT=8080
fi


if [ "$ENVIRONMENT" == "production" ]; then
    echo "Starting production mode!"
    waitress-serve --port=$PORT "app"
else
    echo "Starting development mode!"
    flask run -p $PORT -h $HOST
fi
