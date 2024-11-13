docker rm  -f hello_docker_container
docker rmi -f hello_docker_image

docker build -t hello_docker_image .
docker run --name hello_docker_container -p 8000:8000 -d hello_docker_image