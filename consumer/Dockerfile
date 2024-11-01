FROM python:3-slim
WORKDIR /app
COPY consumer.py .
RUN pip install kafka-python pandas requests
CMD ["python", "consumer.py"]
