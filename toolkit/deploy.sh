#!/bin/bash
echo "Deploying ZephyraCore..."
docker-compose down
docker-compose build
docker-compose up -d
echo "Deployment complete."
