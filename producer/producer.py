# from kafka import KafkaProducer
# import csv
# import time
# import json

# def produce_messages(file_path, topic):
#     producer = KafkaProducer(bootstrap_servers='localhost:9092',api_version=(0, 10, 1), 
#                              value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
#     with open(file_path, mode='r') as file:
#         csv_reader = csv.DictReader(file)
#         for row in csv_reader:
#             producer.send(topic, value=row)
#             print(f"Produced: {row}")
#             time.sleep(2)

# if __name__ == "__main__":
#     produce_messages('wine_demand_data.csv', 'wine_demand')


from kafka import KafkaProducer
import pandas as pd
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',api_version=(0, 10, 1),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Read restaurant data
restaurant_df = pd.read_csv('restaurant_data.csv')
supplier_df = pd.read_csv('supplier_data.csv')

# Send data to Kafka topics
def send_data(df, topic):
    for _, row in df.iterrows():
        data = row.to_dict()
        producer.send(topic, value=data)
        time.sleep(1)  # Simulate data sending interval

# Send restaurant and supplier data
send_data(restaurant_df, 'restaurant_demand')
send_data(supplier_df, 'supplier_offers')

producer.flush()
producer.close()
