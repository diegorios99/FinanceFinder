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
    
    # Apply thresholding (Binarization)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Optionally apply additional denoising if needed
    # thresh = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
    
    # Convert back to PIL image
    img = Image.fromarray(thresh)

    # Optionally enhance sharpness/contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Increase contrast
    
    return img

def clean_text(text):
    # Remove unwanted line breaks between numbers and currency symbols
    text = re.sub(r'(\$\d+)\s+(\d+)', r'\1\2', text)  # Fix "$4" and "00" split into "$4.00"
    return text

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

        # Preprocess the image for better OCR accuracy
        image = preprocess_image(image_stream)

        # Extract text using OCR
        custom_oem_psm_config = r'--oem 3 --psm 6'  # LSTM OCR engine, assume a uniform block of text
        extracted_text = pytesseract.image_to_string(image, config=custom_oem_psm_config)
        print(f"✅ Extracted text: {extracted_text}")

        # Clean up the extracted text (e.g., fix price splits)
        cleaned_text = clean_text(extracted_text)

        # Save extracted text to the database
        try:
            sql = "INSERT INTO receipts (image_filename, extracted_text) VALUES (%s, %s)"
            cursor.execute(sql, (file.filename, cleaned_text))
            db.commit()
            print("✅ Data inserted into the database successfully")

            # Process the cleaned text to extract items and prices
            # Here, you should implement a more sophisticated parsing method based on your receipt structure
            # For simplicity, let's assume we just extract some items from the text
            items = []
            for line in cleaned_text.split("\n"):
                # Example: simple parsing of lines containing '$' symbol (you may need more advanced parsing)
                if '$' in line:
                    # Parse item name, price, and quantity (this is a very basic example)
                    parts = line.split('$')
                    if len(parts) > 1:
                        item_name = parts[0].strip()
                        price = parts[1].strip().replace(",", "")
                        quantity = 1  # Default quantity for now, you can adjust this logic as needed
                        items.append((item_name, price, quantity))
            
            # Insert parsed items into the database
            for item in items:
                item_name, price, quantity = item
                try:
                    item_sql = "INSERT INTO items (item_name, price, quantity, purchase_date) VALUES (%s, %s, %s, CURDATE())"
                    cursor.execute(item_sql, (item_name, price, quantity))
                    db.commit()
                    print(f"✅ Item '{item_name}' added to the items table.")
                except Exception as e:
                    db.rollback()
                    print(f"❌ Error inserting item '{item_name}': {e}")

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
