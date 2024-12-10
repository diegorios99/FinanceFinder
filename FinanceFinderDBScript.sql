CREATE DATABASE receipts_db;

USE receipts_db;

CREATE TABLE receipts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_filename VARCHAR(255),
    extracted_text TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
