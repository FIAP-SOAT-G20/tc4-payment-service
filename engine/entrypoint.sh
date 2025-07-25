#!/usr/bin/env bash

if [[ -z "${HOST}" ]]; then
  export HOST=0.0.0.0
fi

echo "Configuring listener on: $HOST"

if [[ -z "${PORT}" ]]; then
  export PORT=8080
fi


if [ "$ENVIRONMENT" == "production" ]; then
    echo "Starting production mode!"
    waitress-serve --host=$HOST --port=$PORT engine:app
else
    echo "Starting development mode!"
    flask run -p $PORT -h $HOST
fi
