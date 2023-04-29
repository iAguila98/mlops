#!/bin/bash
curl -H "Content-type: application/json" -H "Accept: application/json" -X PATCH --user "airflow:airflow" "http://localhost:8080/api/v1/dags/$1/update_mask=is_paused" -d '{"conf": {}}'