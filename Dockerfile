FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      postgresql-client \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app:create_app

COPY requirements.txt ./
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && rm -rf /root/.cache/pip


COPY . /app
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

