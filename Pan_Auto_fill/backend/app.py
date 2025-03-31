import cv2
import numpy as np
import pytesseract
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from utils import extract_text_from_image

app = Flask(__name__)
CORS(app)

# Load YOLO model
model = YOLO("models/best.pt")

@app.route("/")
def home():
    return render_template("index.html")  # Renders the form UI

@app.route("/extract", methods=["POST"])
def extract_information():
    """Processes the uploaded image and extracts text fields."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    results = model(image)  # YOLO detection
    detected_data = {}

    for result in results:
        for box in result.boxes:
            label = model.names[int(box.cls[0])]  # Fix label extraction
            print(label)
            bbox = box.xyxy[0].tolist()  # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, bbox)

            normalized_label = label.lower().replace(" ", "_")  # Convert to lowercase & replace spaces
            print(normalized_label)
            if normalized_label in ["name", "fathers_name", "dob", "pan_number"]:
                cropped_img = image[y1:y2, x1:x2]
                extracted_text = extract_text_from_image(cropped_img)  
                detected_data[normalized_label] = extracted_text  
                print(f"Extracted '{normalized_label}': {extracted_text}")  # Debugging output

                
            elif label in ["signature", "photo"]:
                detected_data[label] = bbox  # Save bounding box for images
                print(f"Detected {label} at {bbox}")
        print("Detected Data : ",detected_data)

    return jsonify(detected_data)


if __name__ == "__main__":
    app.run(debug=True)
