FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY security_main.py /app/main.py
RUN pip install --no-cache-dir fastapi uvicorn pydantic httpx
EXPOSE 8080
CMD ["python", "main.py"]
