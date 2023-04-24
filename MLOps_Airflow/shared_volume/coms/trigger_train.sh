#!/bin/bash
curl -H "Content-type: application/json" -H "Accept: application/json" -X POST --user "airflow:airflow" "http://localhost:8080/api/v1/dags/$1/dagRuns" -d '{"conf": {}}'

