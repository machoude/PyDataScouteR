FROM python:3.10-slim

WORKDIR /app

RUN pip install fastapi uvicorn pydantic

COPY api/main_simple.py main.py
COPY api/gk_data.json gk_data.json
COPY api/fw_data.json fw_data.json

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
