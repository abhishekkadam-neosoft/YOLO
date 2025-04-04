# 🧾 PAN Card Field Extraction & Auto-Fill System

This project automates the extraction of key fields from Indian PAN (Permanent Account Number) cards using deep learning and OCR, enabling fast and accurate data entry into forms or applications.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution Architecture](#solution-architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)

---

## 🧠 Overview

Manual entry of PAN card details into forms is prone to human error and is inefficient. This project builds a smart system using computer vision and OCR that can detect and extract specific PAN card fields (like Name, PAN Number, Date of Birth) and automatically populate them into a digital form.

---

## ❗ Problem Statement

- Manual PAN card data entry is time-consuming and error-prone.
- Enterprises and service providers require fast, accurate data extraction for onboarding and verification.
- There is a need for a solution that automates this process using machine learning and OCR.

---

    
## ✨ Features

- 🔍 **PAN field detection** using deep learning YOLOV11
- 🧠 **Smart OCR** for clean text extraction
- 🖥️ **Live preview** of PAN card and detected fields
- 📝 **Auto-fills details** into a user form
- 📦 **Easy integration** via API or web interface

---

## ⚙️ Technology Stack

| Component         | Technology        |
|------------------|-------------------|
| Data Annotation   | CVAT              |
| Object Detection  | YOLOv11           |
| OCR               | Pytesseract       |
| Backend           | Python, Flask     |
| Frontend          | Streamlit / HTML  |
| Libraries         | OpenCV, Numpy     |
| Deployment        | Streamlit Cloud / Localhost |

---

## 🏋️ Model Training

### 📌 Data Annotation
- **Tools**: CVAT
- **Classes**: `name`, `father_name`, `pan_number`, `dob` , "image" , "signature"

### 🤖 Model
- **Framework**: YOLOv11 (Ultralytics)
- **Training Epochs**: 50
- **Accuracy**: ~97% mAP


