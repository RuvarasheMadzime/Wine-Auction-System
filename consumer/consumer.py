from kafka import KafkaConsumer
import pandas as pd
import json
import requests
import csv
import random
from datetime import datetime, timedelta

# Initialize Kafka consumer
consumer = KafkaConsumer('restaurant_demand', 'supplier_offers',
                         bootstrap_servers='localhost:9092',
                         api_version=(0, 10, 1),
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

restaurant_data = []
supplier_data = []

# Check feasibility function (MAIN FUNCTION WHERE ALL CALCULATIONS NEED TO HAPPEN)
def check_feasibility(restaurant, supplier):
    return random.choice([True,False])

# Process messages 
for message in consumer:
    data = message.value
    if message.topic == 'restaurant_demand':
        print(f"Received restaurant data: {data}")
        restaurant_data.append(data)
    elif message.topic == 'supplier_offers':
        print(f"Received supplier data: {data}")
        supplier_data.append(data)


