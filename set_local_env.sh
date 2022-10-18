#!/bin/sh

if [ ! -f .env ]; then
  echo 'cannot find .env?'
  return
fi

export PYTHONUNBUFFERED=1
export PYTHONPATH="$( pwd )"

eval $(grep -E 'REDIS|SESSION|POSTGRES|ENVIRONMENT' .env | sed -e 's/^/export /' ) # source session secret and postgresl env

# convert into proper env values
export PGDATABASE="${POSTGRES_DB}"
export PGPASSWORD="${POSTGRES_PASSWORD}"
export PGPORT="${POSTGRES_PORT}"
export PGUSER="${POSTGRES_USER}"

export SQLALCHEMY_DATABASE_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}"