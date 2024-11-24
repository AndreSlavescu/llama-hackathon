from geopy.geocoders import Nominatim
import pandas as pd
from pathlib import Path
import time

geolocator = Nominatim(user_agent="NestQuest")


def get_coordinates(address: str):
    location = geolocator.geocode(address)

    if location:
        return location.longitude, location.latitude
    return None


def main():
    csv_path = Path(__file__).parent.parent.parent / "house_listings.csv"
    print(f"Reading addresses from: {csv_path}")
    
    try:
        listings_df = pd.read_csv(csv_path)
        
        for index, row in listings_df.iterrows():
            address = row["address"]
            coordinates = get_coordinates(address)
            if coordinates:
                print(f"Address: {address}, Coordinates: {coordinates}")
            else:
                print(f"Failed to get coordinates for address: {address}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    main()

