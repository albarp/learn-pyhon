FROM python:3.12-slim-bullseye
WORKDIR /mnt

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*
