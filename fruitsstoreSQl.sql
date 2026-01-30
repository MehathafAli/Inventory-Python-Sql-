CREATE DATABASE fruit_store;
USE fruit_store;

CREATE TABLE fruits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    quantity FLOAT,
    cost_price INT,
    selling_price INT
);

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(10)
);

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    fruit_id INT,
    qty FLOAT,
    total INT,
    sale_date DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (fruit_id) REFERENCES fruits(id)
);
select * from sales;
INSERT INTO fruits (name, quantity, cost_price, selling_price) VALUES
('apple',10,80,100),
('grapes',10,40,60),
('kiwi',10,90,120),
('banana',10,20,30),
('carrot',10,25,35);
select * from fruits