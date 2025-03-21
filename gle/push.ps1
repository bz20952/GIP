# Build app
docker build -t gle-app ./backend

# Push to GHCR
docker tag gle-app:latest ghcr.io/cheshirecat51/gle-app:latest
docker push ghcr.io/cheshirecat51/gle-app:latest

# # Push to ECR
# docker tag gle-app:latest 047719634011.dkr.ecr.eu-north-1.amazonaws.com/gle/app:latest
# docker push 047719634011.dkr.ecr.eu-north-1.amazonaws.com/gle/app:latest

# Build web
docker build -t gle-web ./frontend

# Push to GHCR
docker tag gle-web:latest ghcr.io/cheshirecat51/gle-web:latest
docker push ghcr.io/cheshirecat51/gle-web:latest

# # Push to ECR
# docker tag gle-web:latest 047719634011.dkr.ecr.eu-north-1.amazonaws.com/gle/web:latest
# docker push 047719634011.dkr.ecr.eu-north-1.amazonaws.com/gle/web:latest