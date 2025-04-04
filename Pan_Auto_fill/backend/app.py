import cv2
import numpy as np
import pytesseract
import mysql.connector
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from utils import extract_text_from_image

app = Flask(__name__)
CORS(app)

# Load YOLO model
model = YOLO("models/best.pt")

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "abhishek",
    "database": "pan_database"
}

def save_to_database(data):
    """Insert extracted data into MySQL database."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO pan_details (name, fathers_name, dob, pan_number)
        VALUES (%s, %s, %s, %s)
        """
        values = (data.get("name"), data.get("fathers_name"), data.get("dob"), data.get("pan_number"))

        print("🔥 Executing SQL Query:", sql)  # Debugging
        print("✅ With Values:", values)  # Debugging

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()
        print("✅ Data inserted successfully!")  # Debugging
        return True
    except Exception as e:
        print("❌ Database Error:", e)  # Debugging
        return False
    

@app.route("/")
def home():
    return render_template("index.html")  # Renders the UI

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
            bbox = box.xyxy[0].tolist()  # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, bbox)

            normalized_label = label.lower().replace(" ", "_")  # Convert to lowercase & replace spaces
            if normalized_label in ["name", "fathers_name", "dob", "pan_number"]:
                cropped_img = image[y1:y2, x1:x2]
                extracted_text = extract_text_from_image(cropped_img)  
                detected_data[normalized_label] = extracted_text  

            elif label in ["signature", "photo"]:
                detected_data[label] = bbox  # Save bounding box for images

    return jsonify({"message": "Data extracted!", "data": detected_data})

@app.route("/submit", methods=["POST"])
def submit_information():
    """Saves extracted information into MySQL when the user submits the form."""
    form_data = request.json
    print("🔥 Received Form Data:", form_data)  # Debugging

    if not form_data:
        return jsonify({"error": "No data received"}), 400

    success = save_to_database(form_data)

    if success:
        return jsonify({"message": "✅ Data successfully stored in database!"})
    else:
        return jsonify({"error": "❌ Failed to save data"}), 500



if __name__ == "__main__":
    app.run(debug=True)
