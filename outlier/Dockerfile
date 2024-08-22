# FROM python:3.9
FROM pytorch/pytorch:latest
RUN apt-get update && apt-get upgrade --yes

WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN python -m pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app files
COPY ./app /code/app

# Create a HOME dedicated to the OVHcloud user (42420:42420)
RUN chown -R 42420:42420 /code
ENV HOME=/code

# Run app
CMD ["fastapi", "run", "app/api.py"]