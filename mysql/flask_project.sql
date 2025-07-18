CREATE DATABASE IF NOT EXISTS warehouse_db;

use warehouse_db;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    quantity INT DEFAULT 0
);

CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    location VARCHAR(100),
    stock INT DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE TABLE shipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    direction VARCHAR(10),
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

SHOW TABLES;

ALTER TABLE user MODIFY password VARCHAR(256);

show tables;
