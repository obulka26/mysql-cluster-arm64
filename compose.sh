#!/bin/bash
num_nodes=${1:-1}
nodes_suffix=$(if [ "${num_nodes}" = "1" ]; then echo node; else echo nodes; fi)
#echo ${nodes_suffix}
#echo ${num_nodes}
compose_file="docker-compose-${num_nodes}-${nodes_suffix}.yml"
docker compose -f "${compose_file}" up
docker compose -f "${compose_file}" rm -f
