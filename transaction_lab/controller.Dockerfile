FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /opt/runner
COPY sql_runner/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY sql_runner/__init__.py ./sql_runner/__init__.py
COPY sql_runner/app ./sql_runner/app
COPY sql_runner/resources ./sql_runner/resources
COPY transaction_lab ./transaction_lab
CMD ["uvicorn", "transaction_lab.web:app", "--host", "0.0.0.0", "--port", "8003", "--workers", "1"]
