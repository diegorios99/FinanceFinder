from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image, ImageEnhance
import pymysql
import io
import cv2
import numpy as np
import re

# Configure the path to Tesseract
pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Adjust this path for your OS and installation

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# MySQL configuration
try:
    db = pymysql.connect(host='localhost', user='root', password='password', database='receipts_db')
    cursor = db.cursor()
    print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_stream):
    # Open the image
    img = Image.open(image_stream)
    
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding for dynamic binarization
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Convert back to PIL Image for further processing
    img = Image.fromarray(thresh)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)  # Increase contrast by a factor of 2

    # Enhance sharpness
    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(2.0)  # Increase sharpness by a factor of 2

    return img

def clean_text(text):
    # Remove unwanted line breaks between numbers and currency symbols
    text = re.sub(r'(\$\d+)\s+(\d+)', r'\1\2', text)  # Fix "$4" and "00" split into "$4.00"
    return text

def crop_image(image, left, top, right, bottom):
    """
    Crops the image to the specified region.

    Parameters:
        image (PIL.Image): The image to crop.
        left (int): The left boundary (x-coordinate).
        top (int): The top boundary (y-coordinate).
        right (int): The right boundary (x-coordinate).
        bottom (int): The bottom boundary (y-coordinate).

    Returns:
        PIL.Image: The cropped image.
    """
    return image.crop((left, top, right, bottom))

@app.route('/')
def index():
    print("ℹ️  Accessed the index page")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("ℹ️  Received a file upload request")

    if 'file' not in request.files:
        print("❌ No file part in the request")
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        print("❌ No file selected")
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        print(f"ℹ️  Processing file: {file.filename}")

        # Read the file into memory
        image_stream = io.BytesIO(file.read())

        # Open the image using PIL
        image = Image.open(image_stream)

        # Define the cropping region (adjust these values based on your needs)
        crop_region = (50, 100, 500, 550)  # Example coordinates (left, top, right, bottom)
        cropped_image = crop_image(image, *crop_region)

        # Preprocess the cropped image for better OCR accuracy
        image_buffer = io.BytesIO()
        cropped_image.save(image_buffer, format='PNG')  # Use 'JPEG' if appropriate
        image_buffer.seek(0)  # Reset the buffer's position to the beginning
        processed_image = preprocess_image(image_buffer)


        # Extract text using OCR
        custom_oem_psm_config = r'--oem 3 --psm 6'  # LSTM OCR engine, assume a uniform block of text
        extracted_text = pytesseract.image_to_string(processed_image, config=custom_oem_psm_config, lang='eng')
        print(f"✅ Extracted text: {extracted_text}")

        # Clean up the extracted text
        cleaned_text = clean_text(extracted_text)

        # Save extracted text to the database
        try:
            sql = "INSERT INTO receipts (image_filename, extracted_text) VALUES (%s, %s)"
            cursor.execute(sql, (file.filename, cleaned_text))
            db.commit()
            print("✅ Data inserted into the database successfully")

            return jsonify({'success': True, 'message': 'File processed successfully', 'extracted_text': cleaned_text})

        except Exception as e:
            db.rollback()
            print(f"❌ Database insertion failed: {e}")
            return jsonify({'error': str(e)})

    print("❌ Invalid file type")
    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=False)
