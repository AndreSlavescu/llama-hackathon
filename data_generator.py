import random
import pandas as pd

# Function to generate random house data
def generate_house_data(num_entries=100):
    addresses = [
        f"{random.randint(1, 999)} {random.choice(['King', 'Queen', 'Bay', 'Yonge', 'Dundas', 'Church', 'Bathurst'])} Street, Toronto, Ontario"
        for _ in range(num_entries)
    ]
    prices = [f"${random.randint(400, 4000) * 1000}" for _ in range(num_entries)]
    community_names = ["Corso Italia-Davenport", "Yorkville", "Annex", "East York", "Scarborough", "Etobicoke"]
    mls_numbers = [f"W{random.randint(1000000, 9999999)}" for _ in range(num_entries)]
    bedrooms = [f"{random.randint(2, 5)} + {random.randint(0, 2)}" for _ in range(num_entries)]
    bathrooms = [str(random.randint(1, 4)) for _ in range(num_entries)]
    square_feet = [f"{random.randint(600, 3000)} sqft" if random.random() > 0.3 else "-" for _ in range(num_entries)]
    property_types = ["Single Family", "Condominium", "Townhouse"]
    building_types = ["House", "Condominium", "Townhouse"]
    storeys = [random.randint(1, 3) for _ in range(num_entries)]
    titles = ["Freehold", "Condominium"]
    land_sizes = [f"{random.randint(10, 50)} x {random.randint(50, 150)} FT" for _ in range(num_entries)]
    annual_property_taxes = [f"${random.randint(2000, 15000)}.00" for _ in range(num_entries)]
    total_parking_spaces = [random.randint(0, 4) for _ in range(num_entries)]
    cooling = ["Central air conditioning", "-", "Window Unit"]
    heating_types = ["Forced air (Natural gas)", "Heat Pump", "Radiant Heat"]
    utility_sewer = ["Sanitary sewer", "Municipal sewage system"]
    water = ["Municipal water"]
    exterior_finish = ["Brick", "Stone", "Brick, Stone"]
    time_on_market = [f"{random.randint(1, 120)} days" for _ in range(num_entries)]
    basement_features = ["Separate entrance", "Walk-out", "-", "None"]
    interior_features = ["Hardwood, Ceramic, Laminate", "Vinyl, Concrete", "Central Vacuum, Dishwasher"]
    neighbourhood_amenities = ["Parks, Transit", "Schools, Transit", "Shopping, Hospitals"]
    room_details = [
        "Main Level: Kitchen (10x10), Living Room (15x12)...",
        "Second Level: Bedroom (12x11), Bathroom (8x7)...",
        "Basement: Recreational Room (20x15)..."
    ]

    # Generate data
    data = {
        "Price": random.choices(prices, k=num_entries),
        "Address": random.choices(addresses, k=num_entries),
        "Community Name": random.choices(community_names, k=num_entries),
        "MLS Number": random.choices(mls_numbers, k=num_entries),
        "Bedrooms": random.choices(bedrooms, k=num_entries),
        "Bathrooms": random.choices(bathrooms, k=num_entries),
        "Square Feet": random.choices(square_feet, k=num_entries),
        "Property Type": random.choices(property_types, k=num_entries),
        "Building Type": random.choices(building_types, k=num_entries),
        "Storeys": random.choices(storeys, k=num_entries),
        "Title": random.choices(titles, k=num_entries),
        "Land Size": random.choices(land_sizes, k=num_entries),
        "Annual Property Taxes": random.choices(annual_property_taxes, k=num_entries),
        "Total Parking Spaces": random.choices(total_parking_spaces, k=num_entries),
        "Cooling": random.choices(cooling, k=num_entries),
        "Heating Type": random.choices(heating_types, k=num_entries),
        "Utility Sewer": random.choices(utility_sewer, k=num_entries),
        "Water": random.choices(water, k=num_entries),
        "Exterior Finish": random.choices(exterior_finish, k=num_entries),
        "Time on REALTOR.ca": random.choices(time_on_market, k=num_entries),
        "Basement Features": random.choices(basement_features, k=num_entries),
        "Interior Features": random.choices(interior_features, k=num_entries),
        "Neighbourhood Amenities": random.choices(neighbourhood_amenities, k=num_entries),
        "Room Details": random.choices(room_details, k=num_entries)
    }
    return pd.DataFrame(data)

# Generate dataset for 100 houses
expanded_housing_df = generate_house_data(100)

# Save to CSV
expanded_file_path = "house_listings.csv"
expanded_housing_df.to_csv(expanded_file_path)

expanded_file_path
