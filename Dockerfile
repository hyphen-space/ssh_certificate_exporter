FROM docker.io/library/python:3.13-slim
# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y openssh-client && apt clean && rm -rf /var/lib/apt/lists/*

COPY main.py /app/main.py

EXPOSE 8000

ENTRYPOINT ["python3", "main.py"]
