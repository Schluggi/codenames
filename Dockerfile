FROM python:3.13-alpine
LABEL authors="Schluggi"

WORKDIR /app

COPY codenames /app/codenames
COPY words2img /app/words2img
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt \
    && rm -f /app/requirements.txt
RUN pip install --no-cache-dir gunicorn eventlet


RUN python words2img/words2img.py

EXPOSE 5000
ENTRYPOINT ["gunicorn", "--worker-class", "eventlet", "-w", "2", "-b", "0.0.0.0:5000", "codenames:app"]
