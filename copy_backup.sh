# This will run the keyhole application in the background, copy out the .keyhole
# directory containing the user and password information, then stop the keyhole
# background process.

# Check if Podman is installed, and use it if it is
podman -v
if [ $? == 0 ]
then
  podman run --rm -ti -d --name keyhole -v keyhole_vol:/usr/src/app/.keyhole/ --entrypoint sh keyhole:0.1.3
  podman cp keyhole:/usr/src/app/.keyhole .
  podman stop keyhole -t0
  echo ""
  exit 0
else
  echo "Podman is not installed. Attempting to use Docker."
fi

# Check if Docker is installed, and use it if it is
docker -v
if [ $? == 0 ]
then
  docker run --rm -ti -d --name keyhole -v keyhole_vol:/usr/src/app/.keyhole/ --entrypoint sh keyhole:0.1.3
  docker cp keyhole:/usr/src/app/.keyhole .
  docker stop keyhole -t0
else
  echo "Docker is not installed either. Exiting." 
  echo ""
  exit 1
fi


