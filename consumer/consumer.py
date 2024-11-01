from kafka import KafkaConsumer
import pandas as pd
import json
import requests
import csv
from datetime import datetime, timedelta

# Initialize Kafka consumer
consumer = KafkaConsumer('restaurant_demand', 'supplier_offers',
                         bootstrap_servers='localhost:9092',
                         api_version=(0, 10, 1),
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# API credentials and keys
TOMTOM_API_KEY = 'p2UeB2R48kcOPXXsCG2e0FqY9LOtmkEw'
OPEN_SKY_USERNAME = 'Beel_Ze_BuB07'
OPEN_SKY_PASSWORD = 'Spiderman2.0'

restaurant_data = []
# Load supplier data from CSV
supplier_data = []

# Check feasibility function
def check_feasibility(restaurant, supplier):
    print(f"Checking feasibility for Restaurant: {restaurant['restaurantname']} and Supplier: {supplier['Name']}")
    
    # Check OpenSky API for recent flights
    response = requests.get(
        'https://opensky-network.org/api/flights/departure',
        auth=(OPEN_SKY_USERNAME, OPEN_SKY_PASSWORD),
        params={
            'airport': supplier['airport_name'],
            'begin': int((datetime.now() - timedelta(days=2)).timestamp()),
            'end': int(datetime.now().timestamp())
        }
    )
    flights = response.json()

    # Filter for flights that arrive within 1 hour of restaurant opening
    feasible_flights = [
        flight for flight in flights
        if flight['estArrivalAirport'] == restaurant['airport_name'] and
        datetime.fromtimestamp(flight['lastSeen']) < datetime.strptime(restaurant['Monday_Sun_Times'], '%H:%M') - timedelta(hours=1)
    ]

    print(f"Found {len(feasible_flights)} feasible flights for {restaurant['restaurantname']}.")

    # If no feasible flights, skip
    if not feasible_flights:
        print(f"No feasible flights found for {restaurant['restaurantname']}.")
        return None

    # Check TomTom API for road travel time
    tomtom_url = f"https://api.tomtom.com/routing/1/calculateRoute/{supplier['Latitude']},{supplier['Longitude']}:{restaurant['latitude']},{restaurant['longitude']}/json"
    tomtom_params = {'key': TOMTOM_API_KEY}
    road_response = requests.get(tomtom_url, params=tomtom_params)
    road_data = road_response.json()

    if 'routes' not in road_data or not road_data['routes']:
        print(f"Error retrieving route data from TomTom API for {supplier['Name']} to {restaurant['restaurantname']}.")
        return None

    travel_time = road_data['routes'][0]['summary']['travelTimeInSeconds'] / 60
    traffic_delay = road_data['routes'][0]['summary']['trafficDelayInSeconds'] / 60

    total_travel_time = travel_time + traffic_delay
    print(f"Total travel time from supplier {supplier['Name']} to restaurant {restaurant['restaurantname']}: {total_travel_time} minutes.")

    # Calculate feasibility based on stock availability and timing
    for wine_type in ['request_for_red', 'request_for_white', 'request_for_rose']:
        if restaurant[wine_type] <= supplier[f'Quantity_Available_{wine_type.split("_")[-1].capitalize()}']:
            print(f"Feasibility confirmed for {wine_type.split('_')[-1].capitalize()} wine at {restaurant['restaurantname']}.")
            return {
                'restaurantname': restaurant['restaurantname'],
                'supplier_name': supplier['Name'],
                'wine_type': wine_type.split("_")[-1].capitalize(),
                'quantity': restaurant[wine_type],
                'total_travel_time': total_travel_time,
                'distance': road_data['routes'][0]['summary']['lengthInMeters'] / 1000,
                'traffic_delay': traffic_delay
            }
    print(f"Not enough stock for any wine type at {restaurant['restaurantname']}.")
    return None

# Process messages and calculate feasibility
for message in consumer:
    data = message.value
    if message.topic == 'restaurant_demand':
        print(f"Received restaurant data: {data}")
        restaurant_data.append(data)
    elif message.topic == 'supplier_offers':
        print(f"Received supplier data: {data}")
        supplier_data.append(data)

    feasible_results = []
    for restaurant in restaurant_data:
        for supplier in supplier_data:
            # Ensure the airport names match for both supplier and restaurant
            if restaurant['airport_name'] == supplier['airport_name']:
                print(f"Matching airport names found: {restaurant['airport_name']}")
                result = check_feasibility(restaurant, supplier)
                print(result)
                if result:
                    feasible_results.append(result)
                    print(feasible_results)

    # Write results to CSV
    with open('../results/feasible_auctions.csv', 'w', newline='') as csvfile:
        fieldnames = ['restaurantname', 'supplier_name', 'wine_type', 'quantity', 'total_travel_time', 'distance', 'traffic_delay']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(feasible_results)

    print(f"Feasibility results written to '../results/feasible_auctions.csv'.")
