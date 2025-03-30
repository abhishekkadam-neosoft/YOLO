import streamlit as st
import cv2
import torch
from ultralytics import YOLO
from PIL import Image
import numpy as np

# Load the trained YOLO model
model = YOLO("runs/detect/train6/weights/best.pt")

def detect_objects(frame):
    results = model(frame)
    for r in results:
        annotated_frame = r.plot()
    return annotated_frame

# Set Streamlit page config
st.set_page_config(page_title="PAN Card Field Detection", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Mode", ["Upload Image", "Live Webcam"])

st.title("📄 PAN Card Field Detection App")
st.markdown("### Detect key fields from a PAN card using our Detection Model.")

if app_mode == "Upload Image":
    st.subheader("🖼 Upload an Image for Detection")
    uploaded_file = st.file_uploader("Choose a PAN card image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True, channels="RGB")
        
        # Convert image to numpy array
        image_np = np.array(image)
        
        # Perform object detection
        output_image = detect_objects(image_np)
        
        # Convert back to PIL Image and display
        output_pil = Image.fromarray(output_image)
        st.image(output_pil, caption="Detection Output", use_container_width=True)

elif app_mode == "Live Webcam":
    st.subheader("📷 Live PAN Card Detection")
    
    # Use session state to track webcam status
    if "webcam_running" not in st.session_state:
        st.session_state.webcam_running = False
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Start Webcam", use_container_width=True):
            st.session_state.webcam_running = True
    with col2:
        if st.button("⏹ Stop Webcam", use_container_width=True):
            st.session_state.webcam_running = False
    
    # Start the webcam feed
    if st.session_state.webcam_running:
        cap = cv2.VideoCapture(0)
        stframe = st.empty()
        
        while st.session_state.webcam_running:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture frame. Exiting...")
                break
            
            # Convert BGR to RGB (for Streamlit)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            annotated_frame = detect_objects(frame)
            
            # Convert array to image for Streamlit
            img = Image.fromarray(annotated_frame)
            
            # Display the image
            stframe.image(img, caption="Live Detection", use_container_width=True)
            
            # Stop if the stop button is pressed
            if not st.session_state.webcam_running:
                break
        
        cap.release()
        st.session_state.webcam_running = False
    else:
        st.info("Click 'Start Webcam' to begin detection.")
