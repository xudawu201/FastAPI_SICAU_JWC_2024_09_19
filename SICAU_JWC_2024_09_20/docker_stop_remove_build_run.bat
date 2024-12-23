docker rm  -f sicau_jwc_container
docker rmi -f sicau_jwc_image

docker build -t sicau_jwc_image:v20241219 .
docker run --restart always --name sicau_jwc_container -p 8000:8000 -d sicau_jwc_image:v20241219