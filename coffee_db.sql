DROP DATABASE IF EXISTS coffee_db;
CREATE DATABASE coffee_db;

DROP TABLE IF EXISTS coffee_db.orders;
CREATE TABLE coffee_db.orders (
order_id int PRIMARY KEY AUTO_INCREMENT,
seller_name varchar(255) NOT NULL);

DROP TABLE IF EXISTS coffee_db.order_items;
CREATE TABLE coffee_db.order_items (
item_id int PRIMARY KEY AUTO_INCREMENT,
item_name varchar(255) NOT NULL,
item_type varchar(255) NOT NULL,
cost DECIMAL(10,4),
order_id int NOT NULL,
CONSTRAINT FK_order_items  FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE);