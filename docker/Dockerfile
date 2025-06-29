FROM python:3.12-slim-bullseye
WORKDIR /mnt

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Create a Python virtual environment in /mnt/venv
RUN python -m venv ./venv