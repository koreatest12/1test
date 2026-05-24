FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY fencing_main.py /app/main.py
EXPOSE 8050
CMD ["python", "main.py"]
