FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY upgrade_main.py /app/main.py
RUN pip install --no-cache-dir fastapi uvicorn pydantic httpx
EXPOSE 8060
CMD ["python", "main.py"]
