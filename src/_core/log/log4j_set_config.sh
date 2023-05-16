#!/bin/sh

# ifneq (,$(wildcard ./.env))
#     include .env
#     export
# endif
echo "${PWD}"

export SPARK_CONF_DIR="${PWD}/src/_core/config/local"