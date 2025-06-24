FROM python:3.13-alpine
LABEL authors="Schluggi"

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt \
    && rm -f /app/requirements.txt
RUN pip install gunicorn eventlet

COPY codenames /app/codenames
COPY config.py /app/

EXPOSE 5000
ENTRYPOINT ["gunicorn", "--worker-class", "eventlet", "-w", "2", "-b", "0.0.0.0:5000", "codenames:app"]
