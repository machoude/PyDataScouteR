FROM python:3.10-slim

WORKDIR /app

# Install only what we need
RUN pip install fastapi uvicorn pydantic

# Copy the simple API
COPY api/main_simple.py main.py

# Run it
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
