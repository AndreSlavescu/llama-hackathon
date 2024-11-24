import os
from PIL import Image
import requests
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent
image_dir = REPO_ROOT / "images" / "house4"
image_dir.mkdir(parents=True, exist_ok=True)

if not image_dir.exists():
    raise RuntimeError(f"Failed to create or access directory: {image_dir}")

print(f"Using image directory: {image_dir}")

image_files = [
    f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))
]

if not image_files:
    print("Warning: No images found in directory. Please add some images first.")
    exit(1)

images = [Image.open(os.path.join(image_dir, file)) for file in image_files]

print(f"Loaded {len(images)} images for house1.")

base_url = "http://127.0.0.1:8000"

image_paths = []

for i, image in enumerate(images):
    temp_file = f"temp_image_{i}.png"
    image.save(temp_file)

    with open(temp_file, "rb") as f:
        files = {"image": (os.path.basename(temp_file), f, "image/webp")}

        response = requests.post(f"{base_url}/upload-image", files=files)

        if response.status_code == 200:
            image_path = response.json()["image_path"]
            image_paths.append(image_path)
            print(f"Successfully uploaded image {i+1}: {image_path}")
        else:
            print(f"Failed to upload image {i+1}: {response.status_code}")

    os.remove(temp_file)

if image_paths:
    property_data = {
        "address": "99 Harbour Sq Toronto, ON M5J 2H2",
        "sqft": 1400,
        "price": 1739000.00,
        "image_paths": image_paths,
        "metadata": {},
    }

    response = requests.post(
        f"{base_url}/create",
        json=property_data,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        print("Successfully created property:", response.json())
    else:
        print(f"Failed to create property: {response.status_code}")
        print("Response:", response.text)
