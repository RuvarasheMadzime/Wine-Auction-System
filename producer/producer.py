from kafka import KafkaProducer
import pandas as pd
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',api_version=(0, 10, 1),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Read restaurant data
restaurant_df = pd.read_csv('./data/restaurant_data.csv')
supplier_df = pd.read_csv('./data/supplier_data.csv')

# Send data to Kafka topics
def send_data(df, topic):
    for _, row in df.iterrows():
        data = row.to_dict()
        producer.send(topic, value=data)
        time.sleep(1)  # Simulate data sending interval

# Send restaurant and supplier data
send_data(restaurant_df, 'restaurant_demand')
send_data(supplier_df, 'supplier_offers')

# producer.flush()
# producer.close()
