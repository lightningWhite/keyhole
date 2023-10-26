#!/bin/bash
# This script builds the keyhole application using either Docker or Podman.

# Check if Podman is installed, and use it if it is
podman -v
if [ $? == 0 ]
then
  podman build . -t keyhole:0.1.3
  echo ""
  exit 0
else
  echo "Podman is not installed. Attempting to use Docker."
fi

# Check if Docker is installed, and use it if it is
docker -v
if [ $? == 0 ]
then
  podman build . -t keyhole:0.1.3
else
  echo "Docker is not installed either. Exiting." 
  echo ""
  exit 1
fi

