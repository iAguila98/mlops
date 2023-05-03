#!/bin/bash
curl -H "Content-type: application/json" -H "Accept: application/json" -X GET --user "airflow:airflow" "http://localhost:8080/api/v1/dags/test_models/dagRuns" -d '{"conf": {}}'