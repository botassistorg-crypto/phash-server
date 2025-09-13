import pandas as pd
import requests
from PIL import Image
import imagehash
from io import BytesIO
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

df = pd.read_csv("products.csv")
df.columns = df.columns.str.strip()

hashes = []
for idx, row in df.iterrows():
    image_url = row.get("image_url")
    try:
        response = requests.get(image_url, verify=False, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        phash = str(imagehash.phash(img))
        print(f"Row {idx+1}: {row.get('name', '')} → {phash}")
        hashes.append(phash)
    except Exception as e:
        print(f"⚠️ Error Row {idx+1}: {e}")
        hashes.append(None)

# Store into IMGcode column
df["IMGcode"] = hashes

# Save new file with hashes populated
df.to_csv("products_with_hash.csv", index=False)

print("\n✅ Done! New file saved as products_with_hash.csv")