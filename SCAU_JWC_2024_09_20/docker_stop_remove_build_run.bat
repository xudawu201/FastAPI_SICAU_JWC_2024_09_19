docker rm  -f scau_jwc_container
docker rmi -f scau_jwc_image

docker build -t scau_jwc_image .
docker run --restart always --name scau_jwc_container --network docker_bridge_network -p 8000:8000 -v C:\xudawu\DockerData2024_09_29\scau_jwc_2024_11_01:/scau_jwc/data -d scau_jwc_image