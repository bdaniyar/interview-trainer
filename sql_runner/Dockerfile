FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /opt/runner
COPY sql_runner/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY sql_runner/__init__.py ./sql_runner/__init__.py
COPY sql_runner/app ./sql_runner/app
COPY sql_runner/resources ./sql_runner/resources
EXPOSE 8002
CMD ["uvicorn", "sql_runner.app.main:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "1"]
