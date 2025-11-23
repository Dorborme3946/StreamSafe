from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import base64
from ultralytics import YOLO

# Initialize FastAPI
app = FastAPI()

# CORS (optional, for frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model once at startup
model = YOLO("yolov8n.pt")  # or yolov12n.pt if you have it

@app.post("/process-frame")
async def process_frame(file: UploadFile = File(...)):
    # Read file bytes
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run YOLO detection
    results = model(frame)

    # Blur detected objects
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            roi = frame[y1:y2, x1:x2]
            roi = cv2.GaussianBlur(roi, (51, 51), 30)
            frame[y1:y2, x1:x2] = roi

    # Encode image to base64
    _, buffer = cv2.imencode(".jpg", frame)
    img_b64 = base64.b64encode(buffer).decode("utf-8")

    return {
        "frame": img_b64,
        "size": {"width": frame.shape[1], "height": frame.shape[0]}
    }

# ✅ Root route
@app.get("/")
async def root():
    return {"message": "Backend is running!"}
