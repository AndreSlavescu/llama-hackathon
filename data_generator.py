import random
import pandas as pd
import json

def generate_house_data(num_entries=100):
    # Base data generation
    addresses = [
        f"{random.randint(1, 999)} {random.choice(['King', 'Queen', 'Bay', 'Yonge', 'Dundas', 'Church', 'Bathurst'])} Street, Toronto, Ontario"
        for _ in range(num_entries)
    ]
    square_feet = [random.randint(600, 3000) for _ in range(num_entries)]
    prices = [random.randint(400, 4000) * 1000 for _ in range(num_entries)]
    image_folders = ["images/house1", "images/house2", "images/house3"]
    image_sets = [", ".join([f"{folder}/{i}.jpg" for i in range(1, 11)]) for folder in image_folders]

    # Metadata fields
    metadata_entries = []
    
    for _ in range(num_entries):
        metadata = {
            "bedrooms": f"{random.randint(2, 5)} + {random.randint(0, 2)}",
            "bathrooms": str(random.randint(1, 4)),
            "property_type": random.choice(["Single Family", "Condominium", "Townhouse"]),
            "building_type": random.choice(["House", "Condominium", "Townhouse"]),
            "storeys": random.randint(1, 3),
            "title": random.choice(["Freehold", "Condominium"]),
            "land_size": f"{random.randint(10, 50)} x {random.randint(50, 150)} FT",
            "annual_property_taxes": f"${random.randint(2000, 15000)}.00",
            "total_parking_spaces": random.randint(0, 4),
            "cooling": random.choice(["Central air conditioning", "-", "Window Unit"]),
            "heating_type": random.choice(["Forced air (Natural gas)", "Heat Pump", "Radiant Heat"]),
            "utility_sewer": random.choice(["Sanitary sewer", "Municipal sewage system"]),
            "water": "Municipal water",
            "exterior_finish": random.choice(["Brick", "Stone", "Brick, Stone"]),
            "time_on_market": f"{random.randint(1, 120)} days",
            "basement_features": random.choice(["Separate entrance", "Walk-out", "-", "None"]),
            "interior_features": random.choice([
                "Hardwood, Ceramic, Laminate",
                "Vinyl, Concrete",
                "Central Vacuum, Dishwasher"
            ]),
            "neighbourhood_amenities": random.choice([
                "Parks, Transit",
                "Schools, Transit",
                "Shopping, Hospitals"
            ])
        }
        metadata_entries.append(json.dumps(metadata))
    
    # Create DataFrame with the new structure
    data = {
        "address": addresses,
        "sqft": square_feet,
        "price": prices,
        "images": random.choices(image_sets, k=num_entries),
        "metadata": metadata_entries
    }
    
    return pd.DataFrame(data)

# Generate dataset for 100 houses
housing_df = generate_house_data(100)

# Save to CSV
file_path = "house_listings.csv"
housing_df.to_csv(file_path)