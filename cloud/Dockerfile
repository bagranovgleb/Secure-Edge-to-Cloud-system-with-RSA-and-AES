FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir flask cryptography

# Only copy what the Cloud needs
COPY common/ /app/common/
COPY cloud/cloud_app.py /app/

ENV PYTHONPATH="/app"

EXPOSE 5000
CMD ["python", "cloud_app.py"]