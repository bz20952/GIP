docker build -t gle-app ./backend
docker tag gle-app:latest ghcr.io/cheshirecat51/gle-app:latest
docker push ghcr.io/cheshirecat51/gle-app:latest

docker build -t gle-web ./frontend
docker tag gle-web:latest ghcr.io/cheshirecat51/gle-web:latest
docker push ghcr.io/cheshirecat51/gle-web:latest