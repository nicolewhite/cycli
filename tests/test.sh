#!/usr/bin/env bash
curl -u neo4j:neo4j --data "password=password" http://localhost:7474/user/neo4j/password
make test