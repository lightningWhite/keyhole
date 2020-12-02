# This will run the keyhole application in the background, copy out the .keyhole
# directory containing the user and password information, then stop the keyhole
# background process.

docker run --rm -ti -d --name keyhole -v keyhole_vol:/usr/src/app/.keyhole/ --entrypoint sh keyhole:0.1.1
docker cp keyhole:/usr/src/app/.keyhole .
docker stop keyhole
