FROM python:3.9

# Create and set the HOME directory
WORKDIR /workspace
ENV HOME=/workspace

# Add our job's file to this directory
ADD . /workspace

# Give the OVHcloud user (42420:42420) access to this directory
RUN chown -R 42420:42420 /workspace

# Install required packages and libraries
RUN apt-get update && apt-get install --yes
RUN pip install -r requirements.txt

# Install dependencies
# RUN apt-get update && apt-get upgrade --yes
# RUN python -m pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Run app
CMD ["fastapi", "run", "/workspace/api.py"]