#!/bin/bash

# Assuming NEOMODEL_NEO4J_AUTH_USERNAME and NEOMODEL_NEO4J_AUTH_PASSWORD are passed as environment variables
export NEO4J_AUTH="${NEOMODEL_NEO4J_AUTH_USERNAME}:${NEOMODEL_NEO4J_AUTH_PASSWORD}"

# Now, run the main container process
exec "$@"

# neo4jdb/start-neo4j.sh