FROM python:3.9

RUN apt-get update && \
    apt-get upgrade --yes

RUN useradd --create-home sirius
USER sirius
WORKDIR /code

ENV VIRTUALENV=/code/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=sirius ./requirements.txt /code/requirements.txt
RUN python -m pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY --chown=sirius ./app /code/app
#CMD ["uvicorn", "app.main:app", "--reload"]
#CMD ["gunicorn", "app.main:app", "-w", "4" "-k", "uvicorn.workers.UvicornWorker"]
CMD ["fastapi", "run", "app/main.py"]