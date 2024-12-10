from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import pymysql
import io

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
        image = Image.open(image_stream)

        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(image)
        print(f"✅ Extracted text: {extracted_text}")

        # Save extracted text to database
        try:
            sql = "INSERT INTO receipts (image_filename, extracted_text) VALUES (%s, %s)"
            cursor.execute(sql, (file.filename, extracted_text))
            db.commit()
            print("✅ Data inserted into the database successfully")
            return jsonify({'success': True, 'message': 'File processed successfully', 'extracted_text': extracted_text})
        except Exception as e:
            db.rollback()
            print(f"❌ Database insertion failed: {e}")
            return jsonify({'error': str(e)})

    print("❌ Invalid file type")
    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True)
