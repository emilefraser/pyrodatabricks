#!/bin/bash
ws_name="${1}"

databricks workspace ls "${ws_name}" --profile "DEFAULT"
