import requests
import base64

# URL of your FastAPI backend
url = "http://127.0.0.1:8000/process-frame"

# Path to your test image
image_path = "image/test_upload.png"  # adjust path if needed

# Open the image in binary mode
with open(image_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    img_b64 = data["frame"]
    
    # Decode base64 back to bytes
    img_bytes = base64.b64decode(img_b64)
    
    # Save to a new file
    output_path = "image/test_upload_blurred.png"
    with open(output_path, "wb") as out:
        out.write(img_bytes)
    
    print(f"Blurred image saved to {output_path}")
else:
    print("Error:", response.status_code, response.text)
