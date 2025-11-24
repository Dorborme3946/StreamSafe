from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import base64
from roboflow import Roboflow

# --------------------------- Roboflow setup ---------------------------
rf = Roboflow(api_key="l9cfcKbJNSCFHSuaFscE")  # replace with your API key
project = rf.workspace("streamsafe").project("find-credit-cards")
model = project.version(1).model  # use the correct version

# --------------------------- FastAPI setup ---------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------- Endpoint ---------------------------
@app.post("/process-frame")
async def process_frame(file: UploadFile = File(...)):
    # Read image from upload
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Save temporary file to send to Roboflow
    temp_path = "temp.jpg"
    cv2.imwrite(temp_path, frame)

    # Send frame to Roboflow model
    result = model.predict(temp_path, confidence=40, overlap=30).json()  # adjust confidence if needed

    # Blur detected credit cards
    for detection in result["predictions"]:
        x, y, w, h = detection["x"], detection["y"], detection["width"], detection["height"]
        x1, y1 = int(x - w / 2), int(y - h / 2)
        x2, y2 = int(x + w / 2), int(y + h / 2)

        roi = frame[y1:y2, x1:x2]
        roi = cv2.GaussianBlur(roi, (51, 51), 30)
        frame[y1:y2, x1:x2] = roi

    # Encode image to base64
    _, buffer = cv2.imencode(".jpg", frame)
    img_b64 = base64.b64encode(buffer).decode("utf-8")

    return {
        "frame": img_b64,
        "size": {"width": frame.shape[1], "height": frame.shape[0]},
        "detections": result["predictions"]
    }

# --------------------------- Root endpoint ---------------------------
@app.get("/")
async def root():
    return {"message": "Backend running!"}
