FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app
ENV FLASK_APP=app:create_app

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

