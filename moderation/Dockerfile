FROM python:3.9
RUN apt-get update && \
    apt-get upgrade --yes

# Create sirius user
#RUN useradd --create-home sirius
#USER sirius

# Copy app files
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

# Create a HOME dedicated to the OVHcloud user (42420:42420)
RUN chown -R 42420:42420 /code
ENV HOME=/code

# Create virtual environment
#ENV VIRTUALENV=/code/venv
#RUN python3 -m venv $VIRTUALENV
#ENV PATH="$VIRTUALENV/bin:$PATH"

# Install dependencies
RUN python -m pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Run app
CMD ["fastapi", "run", "app/api.py"]