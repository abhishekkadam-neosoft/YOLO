import cv2
import pytesseract

# Set the full path to the Tesseract executable(Linux)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# # Set the full path to the Tesseract executable(Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(cropped_image):
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Improve contrast
    return pytesseract.image_to_string(binary, config="--psm 6").strip()

