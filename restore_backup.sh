# This will run the keyhole application in the background, copy in a specified
# backup of a .keyhole directory containing the user and password information,
# then stop the keyhole background process.

# This requires an argument for the path to  the .keyhole directory to restore.

# Check if Podman is installed, and use it if it is
podman -v
if [ $? == 0 ]
then
  podman run --rm -ti -d --name keyhole -v keyhole_vol:/usr/src/app/.keyhole/ --entrypoint sh keyhole:0.1.3
  podman cp .keyhole keyhole:/usr/src/app/
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
  docker cp .keyhole keyhole:/usr/src/app/
  docker stop keyhole -t0
else
  echo "Docker is not installed either. Exiting." 
  echo ""
  exit 1
fi


