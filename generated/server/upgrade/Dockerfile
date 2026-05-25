FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY upgrade_main.py main.py
EXPOSE 8060
CMD ["python", "main.py"]
