'''import requests
import base64
import cv2
import numpy as np

url = "http://127.0.0.1:8000/process-frame"

# Replace with your test image path
files = {"file": open("image/test_upload.png", "rb")}

response = requests.post(url, files=files)
data = response.json()

# Decode and display
img_data = base64.b64decode(data["frame"])
nparr = np.frombuffer(img_data, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow("Processed Frame", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''