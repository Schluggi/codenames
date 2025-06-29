FROM python:3.13-alpine
LABEL authors="Schluggi"

WORKDIR /app

COPY codenames /app/codenames
COPY tools /app/tools
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade --root-user-action pip gunicorn eventlet
RUN pip install --no-cache-dir --upgrade --root-user-action -r /app/requirements.txt \
    && rm -f /app/requirements.txt

RUN python tools/words_to_image.py

EXPOSE 5000
ENTRYPOINT ["gunicorn", "--worker-class", "eventlet", "-w", "2", "-b", "0.0.0.0:5000", "codenames:app"]
