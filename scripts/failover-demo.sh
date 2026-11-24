#!/usr/bin/env bash
# Prints which cluster answers, once per second. Stop/start the private cluster while it runs.
while true; do
  printf '%s  ' "$(date +%T)"
  curl -s -m 3 http://localhost:8080/info || echo "NO RESPONSE"
  echo
  sleep 1
done
