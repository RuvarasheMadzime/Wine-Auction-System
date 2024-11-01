#make sure all requests is installed
import requests

# API Key for DistanceMatrix.ai
API_KEY = 'ikuA7PyvI4RnBvxUIWzoKpkupymoGD5kMpDTaJztvsxs14vi74N9zig7WXw7dHFa'

# Parameters for general cost calculation
FUEL_PRICE_PER_LITER = 23.00  # Variable: update as needed
FUEL_CONSUMPTION_RATE = 12.0  # km per liter
WEAR_AND_TEAR_COST_PER_KM = 1.50  # Adjust as needed
AVERAGE_TOLL_COST_PER_100KM = 20.00  # Approximate toll cost per 100km

def get_distance_data(supplier_location, restaurant_location):
    """
    Retrieve distance and duration from DistanceMatrix.ai API.
    """
    url = f"https://api.distancematrix.ai/maps/api/distancematrix/json"
    params = {
        "origins": f"{supplier_location['latitude']},{supplier_location['longitude']}",
        "destinations": f"{restaurant_location['latitude']},{restaurant_location['longitude']}",
        "key": API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        distance_km = data['rows'][0]['elements'][0]['distance']['value'] / 1000
        duration_sec = data['rows'][0]['elements'][0]['duration']['value']
        return distance_km, duration_sec
    else:
        raise Exception("API request failed with status:", data['status'])

def calculate_road_delivery_cost(distance_km):
    """
    Calculate the total road delivery cost based on:
    - Fuel costs
    - Wear and tear per km
    - Estimated toll costs
    """
    # Fuel cost
    liters_needed = distance_km / FUEL_CONSUMPTION_RATE
    fuel_cost = liters_needed * FUEL_PRICE_PER_LITER
    
    # Wear and tear cost
    wear_and_tear_cost = distance_km * WEAR_AND_TEAR_COST_PER_KM
    
    # Toll cost estimation (assume a toll for every 100 km)
    toll_cost = (distance_km / 100) * AVERAGE_TOLL_COST_PER_100KM
    
    # Total road cost
    total_cost = fuel_cost + wear_and_tear_cost + toll_cost
    return total_cost

def financial_analysis(supplier, restaurant):
    # Retrieve distance and duration between supplier and restaurant
    distance_km, duration_sec = get_distance_data(supplier, restaurant)
    
    # Calculate road delivery cost
    road_cost = calculate_road_delivery_cost(distance_km)
    
    # Display analysis report
    print("----- Delivery Feasibility Report -----")
    print(f"Supplier: {supplier['name']} - Location: {supplier['location']}")
    print(f"Restaurant: {restaurant['name']} - Location: {restaurant['location']}")
    print(f"Distance: {distance_km:.2f} km")
    print(f"Estimated Road Delivery Cost: R{road_cost:.2f}")
    print("Cost Breakdown:")
    print(f"  Fuel Cost: R{(distance_km / FUEL_CONSUMPTION_RATE) * FUEL_PRICE_PER_LITER:.2f}")
    print(f"  Wear and Tear: R{distance_km * WEAR_AND_TEAR_COST_PER_KM:.2f}")
    print(f"  Toll Costs: R{(distance_km / 100) * AVERAGE_TOLL_COST_PER_100KM:.2f}")
    print("---------------------------------------")

# Example Supplier and Restaurant Data
supplier = {
    "name": "Vineyard Vintages",
    "location": "Stellenbosch",
    "latitude": -33.9323,
    "longitude": 18.8555,
}

restaurant = {
    "name": "Cape Bistro",
    "location": "Cape Town",
    "latitude": -33.9258,
    "longitude": 18.4233,
}

# Run the financial analysis
financial_analysis(supplier, restaurant)
