# This script will start the keyhole application with either
# docker or podman depending on which is installed

# Check if Podman is installed, and use it if it is
podman -v
if [ $? == 0 ]
then
  podman run --rm -ti --name keyhole -v keyhole_vol:/usr/src/app/.keyhole/ keyhole:0.1.2
  echo ""
  exit 0
else
  echo "Podman is not installed. Attempting to use Docker."
fi

# Check if Docker is installed, and use it if it is
docker -v
if [ $? == 0 ]
then
  docker run --rm -ti --name keyhole -v keyhole_vol:/usr/src/app/.keyhole/ keyhole:0.1.2
else
  echo "Docker is not installed either. Exiting." 
  echo ""
  exit 1

fi

