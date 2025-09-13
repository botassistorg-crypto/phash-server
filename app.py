from fastapi import FastAPI, Query
import requests
from PIL import Image
import imagehash
from io import BytesIO
import urllib3

# Disable insecure request warnings (since we are ignoring SSL problems)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create the FastAPI app
app = FastAPI()

# Simple health check endpoint
@app.get("/")
def health():
    return {"status": "ok"}

# Endpoint to calculate perceptual hash
@app.get("/getPhash")
def get_phash(image_url: str = Query(..., description="URL of the image")):
    try:
        # Download the image but skip SSL verification
        response = requests.get(image_url, verify=False)
        response.raise_for_status()

        # Open with Pillow
        img = Image.open(BytesIO(response.content))

        # Calculate perceptual hash
        phash = str(imagehash.phash(img))

        return {"phash": phash}
    except Exception as e:
        return {"error": str(e)}