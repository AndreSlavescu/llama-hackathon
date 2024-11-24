import pandas as pd
import requests
from pathlib import Path
import os
from PIL import Image

REPO_ROOT = Path.cwd()
print(REPO_ROOT)
csv_path = REPO_ROOT / "house_listings.csv"
print(f"Looking for CSV at: {csv_path}")
listings_df = pd.read_csv(csv_path)

base_url = "http://127.0.0.1:8000"

for index, row in listings_df.iterrows():
    index_mod = index % 3
    print(f"\nProcessing property {index_mod + 1}")
    property_image_dir = REPO_ROOT / "images" / f"house{index_mod + 1}"
    print(f"Checking directory: {property_image_dir}")

    if not property_image_dir.exists():
        print(
            f"Warning: No image directory found for house{index_mod + 1}, skipping..."
        )
        continue

    image_files = [
        f
        for f in os.listdir(property_image_dir)
        if os.path.isfile(os.path.join(property_image_dir, f))
    ]
    print(f"Found {len(image_files)} images: {image_files}")

    image_paths = []

    for i, image_file in enumerate(image_files):
        print(f"Processing image {i+1}/{len(image_files)}: {image_file}")
        try:
            image = Image.open(os.path.join(property_image_dir, image_file))
            print(f"Successfully opened image: {image.size}, {image.mode}")

            temp_file = f"temp_image_house_{index_mod}_{i}.png"
            print(f"Saving temporary file: {temp_file}")
            image.save(temp_file)
            print("Temporary file saved successfully")

            with open(temp_file, "rb") as f:
                files = {"image": (os.path.basename(temp_file), f, "image/png")}
                print(f"Sending POST request to {base_url}/upload-image")
                response = requests.post(f"{base_url}/upload-image", files=files)

                if response.status_code == 200:
                    image_path = response.json()["image_path"]
                    image_paths.append(image_path)
                    print(
                        f"Successfully uploaded image {i+1} for house{index_mod + 1}: {image_path}"
                    )
                else:
                    print(
                        f"Failed to upload image {i+1} for house{index_mod + 1}: {response.status_code}"
                    )

            os.remove(temp_file)
        except Exception as e:
            print(f"Failed to process image {i+1} for house{index_mod + 1}: {e}")

    property_data = {
        "address": row["address"],
        "sqft": row["sqft"],
        "price": row["price"],
        "image_paths": image_paths,
        "metadata": {},
    }

    response = requests.post(
        f"{base_url}/create",
        json=property_data,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        print(f"Successfully created property {index_mod + 1}:", response.json())
    else:
        print(f"Failed to create property {index_mod + 1}: {response.status_code}")
        print("Response:", response.text)
