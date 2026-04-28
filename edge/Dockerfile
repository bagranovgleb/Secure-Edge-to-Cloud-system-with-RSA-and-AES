FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir cryptography requests
COPY common/ /app/common/
COPY edge/ /app/
# Change CMD to run the bootloader
CMD ["python", "bootloader.py"]