CREATE DATABASE IF NOT EXISTS coffee_db;

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


SELECT orders.seller_name, COUNT(orders.seller_name), SUM(order_items.cost)
FROM coffee_db.orders as orders INNER JOIN coffee_db.order_items as order_items on
coffee_db.orders.order_id = coffee_db.order_items.order_id
GROUP BY orders.seller_name;