#!/bin/bash

folder="${1}"
databricks workspace delete "${folder} --recursive"


