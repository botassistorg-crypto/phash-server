import pandas as pd
import requests
from PIL import Image
import imagehash
from io import BytesIO
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load CSV
df = pd.read_csv("products.csv")

# Strip whitespace from all column headers
df.columns = df.columns.str.strip()

print("Cleaned columns:", df.columns.tolist())

for idx, row in df.iterrows():
    # Now it will use the cleaned header names
    product_name = row.get("name", f"Row {idx+1}")
    image_url = row.get("image_url")
    expected_hash = str(row.get("IMGcode")) if "IMGcode" in df.columns and pd.notna(row.get("IMGcode")) else None

    print(f"\nRow {idx+1}: {product_name}")
    print(f"Image URL: {image_url}")

    try:
        response = requests.get(image_url, verify=False, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        phash = str(imagehash.phash(img))
        print(f"Generated pHash: {phash}")

        if expected_hash and phash.lower() == expected_hash.lower():
            print("✅ MATCHES the IMGcode in sheet")
        else:
            print(f"❌ DOES NOT MATCH (Sheet IMGcode: {expected_hash})")
    except Exception as e:
        print(f"⚠️ Error: {e}")