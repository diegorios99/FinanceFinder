# FinanceFinder

FinanceFinder is a Flask-based web application designed to upload receipt images, extract item details using OCR (Optical Character Recognition), and store the extracted information in a MySQL database. This tool helps track expenses by identifying individual items from receipts and logging them automatically.

---

## Table of Contents

1. [Features](#features)  
2. [Technologies Used](#technologies-used)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Folder Structure](#folder-structure)  
6. [Database Schema](#database-schema)  
7. [Local Hosting and Network Access](#local-hosting-and-network-access)  
8. [Troubleshooting](#troubleshooting)  
9. [Future Improvements](#future-improvements)  
10. [License](#license)  

---

## Features

- **Receipt Upload**: Upload receipt images directly from your computer or mobile device.  
- **Image Preview**: View a preview of the selected image before uploading.  
- **OCR Processing**: Extract text and item details (e.g., item name, price, quantity) from receipts using Tesseract OCR.  
- **Database Storage**: Store extracted information in a MySQL database (`receipts` and `items` tables).  
- **Expense Tracking**: Track individual items purchased, including their price and quantity.  
- **Local Network Access**: Access the app from your phone or other devices within your local network.  

---

## Technologies Used

- **Backend**: Flask (Python)  
- **Frontend**: HTML, CSS, JavaScript  
- **OCR**: Tesseract OCR  
- **Database**: MySQL  
- **Image Processing**: OpenCV, PIL (Python Imaging Library)  

---

## Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/FinanceFinder.git
cd FinanceFinder
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- Windows 
```bash
venv\Scripts\activate
```

- macOS/Linux 
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Install Tesseract OCR
Tesseract OCR is required to process the receipt images.

- Windows:

    1. Download and install Tesseract OCR from Tesseract's GitHub.

    2. Add Tesseract to your system `PATH`.

    3. Set the Tesseract path in `app.py` (Note that mine is in the `D:` drive, install yours acordingly):
        ```bash
        pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        ```
- macOS(Homebrew):
    ```bash
    brew install tesseract
    ```
- Linux(Ubuntu):
    ```bash
    sudo apt-get install tesseract-ocr
    ```

### 6. Set up MySQL Database

1. Start your MySQL server.
2. Run the following SQL script to create the database and tables.
    ```sql
    CREATE DATABASE receipts_db;

    USE receipts_db;

    CREATE TABLE receipts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        image_filename VARCHAR(255),
        extracted_text TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(255),
        price DECIMAL(10, 2),
        quantity INT,
        purchase_date DATE
    );
    ```

### 7. Run the Flask App Locally
Start the Flask application by running the following command:

    ```bash
    python app.py
    ```

The app should be running at:

    ```arduino
    http://127.0.0.1:5000
    ```

To access the app from your phone on the same network, find your local IP address and use:

    ```perl
    http://<your-local-ip>:5000
    ```

Example: `http://192.168.0.119:5000`

## Usage
1. Upload a Receipt:

    - Select an image of a receipt using the "Choose Image" button.
    - View the image preview to confirm the correct file.
    - Click "Upload" to process the receipt.
2. View Extracted Text:
    - The extracted text from the receipt will be displayed on the page.
    - Individual items are parsed and stored in the database.
3. Check Database:

    - Verify stored items by accessing the `/items` route:
    ```arduino
    http://127.0.0.1:5000/items
    ```

## Folder Structure
```lua
FinanceFinder/
│-- app.py
│-- FinanceFinderDBScript.sql
│-- requirements.txt
│-- templates/
│   ├── index.html
│   ├── styles.css
│   └── scripts.js
└-- static/
    ├── styles.css
    └── scripts.js
```

## Database Schema

### `receipts` Table

| **Column**       | **Type**          | **Description**                         |
|------------------|-------------------|-----------------------------------------|
| `id`            | INT (PK)          | Auto-incrementing receipt ID            |
| `image_filename`| VARCHAR(255)      | Name of the uploaded image              |
| `extracted_text`| TEXT              | Extracted text from the receipt         |
| `uploaded_at`   | TIMESTAMP         | Timestamp of when the receipt was uploaded |

### `items` Table

| **Column**       | **Type**          | **Description**                         |
|------------------|-------------------|-----------------------------------------|
| `id`            | INT (PK)          | Auto-incrementing item ID               |
| `item_name`     | VARCHAR(255)      | Name of the purchased item              |
| `price`         | DECIMAL(10, 2)    | Price of the item                       |
| `quantity`      | INT               | Quantity of the item                    |
| `purchase_date` | DATE              | Date of purchase                        |


## Local Hosting and Network Access

### Access the App on Your Local Network 

1. **Modify** `app.py` to allow network access:
    ```python
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=False)
    ```
2. Find Your Local IP Address:

- Windows: Run `ipconfig` in Command Prompt.
- macOS/Linux: Run `ifconfig` in Terminal.

3. Access the App on Your Phone:
Ensure your phone and computer are on the **same Wi-Fi network**, then open:

    ```
    http://<your-local-ip>:5000
    ```
    Example:
    ```
    http://192.168.0.119:5000
    ```

### Troubleshooting
- Bad Request Errors: Ensure you're accessing the app via http:// and not https://.
- Tesseract Not Found: Verify the Tesseract installation path in app.py.
- Database Connection Issues: Confirm MySQL is running and credentials are correct in app.py.
- Firewall Issues: Ensure your firewall allows incoming connections on port 5000.
- MySQL root credentials may be incorrect, verify that you are using the appropriate password.

### Future Improvements
- Add user authentication for secure access.
- Implement better error handling and logging.
- Enhance OCR accuracy with preprocessing techniques.
- Improve UI/UX for a more modern experience.

### License
```## License

MIT License

Copyright (c) 2024 diegorios99 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
