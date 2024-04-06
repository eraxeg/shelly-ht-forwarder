FROM python:3.9-slim

WORKDIR /app

COPY forwarding_service.py .

CMD ["python", "forwarding_service.py"]
