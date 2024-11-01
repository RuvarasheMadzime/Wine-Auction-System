FROM python:3-slim
WORKDIR /app
COPY producer.py .
COPY ../data/restaurant_data.csv .
COPY ../data/supplier_data.csv .
RUN pip install kafka-python pandas
CMD ["python", "producer.py"]

