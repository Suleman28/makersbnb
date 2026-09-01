#!/usr/bin/env bash
set -euo pipefail

ENV_FILE=".env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "No .env file found. Copy .example.env to .env and fill it in, then re-run this script." >&2
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

create_db_if_missing() {
  local env_var="$1"
  local url="${!env_var:-}"

  if [[ -z "$url" ]]; then
    echo "$env_var is not set in .env. See .example.env." >&2
    exit 1
  fi

  local name="${url##*/}"

  if psql -lqt | cut -d '|' -f 1 | grep -qw "$name"; then
    echo "Database '$name' already exists, skipping."
  else
    echo "Creating database '$name'..."
    createdb "$name"
  fi
}

for env_var in DATABASE_URL TEST_DATABASE_URL; do
  create_db_if_missing "$env_var"
done

echo "Done."
