CWD=$(pwd)

docker run \
    --tty \
    --interactive \
    --rm \
    --userns host \
    --user $(id -u $(whoami)) \
    --network=stac-portal_network \
    --publish 8000:8000/tcp \
    --mount type=bind,src=${CWD}/stac_portal,dst=/stac_portal \
    --mount type=bind,src=${CWD}/configurations,dst=/configurations \
    --mount type=bind,src=${CWD}/media_files,dst=/media_files \
    --name=stac_portal_dev \
    --network-alias	django_stac_portal \
    stac-django:latest \
    python /stac_portal/manage.py runserver 0.0.0.0:8000
