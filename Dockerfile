FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install fastapi uvicorn gunicorn
WORKDIR /app
COPY app /app/
RUN pip3 install --no-cache-dir -r requirements.txt && pip3 install uvicorn  

EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"] 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]