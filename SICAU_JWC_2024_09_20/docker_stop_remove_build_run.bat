docker rm  -f sicau_jwc_container
docker rmi -f sicau_jwc_image

docker build -t sicau_jwc_image .
docker run --restart always --name sicau_jwc_container -p 8000:8000 -v C:\xudawu\DockerData2024_09_29\sicau_jwc_2024_11_01:/sicau_jwc/data -d sicau_jwc_image