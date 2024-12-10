#DROP DATABASE receipts_db;
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
