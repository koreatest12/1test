FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY migration_main.py /app/main.py
RUN pip install --no-cache-dir fastapi uvicorn pydantic httpx
EXPOSE 8090
CMD ["python", "main.py"]
