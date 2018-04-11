CREATE DATABASE IF NOT EXISTS coffee_db;

DROP TABLE IF EXISTS coffee_db.salesman;
CREATE TABLE coffee_db.salesman (salesman_number int PRIMARY KEY, seller_name varchar(255) NOT NULL);

DROP TABLE IF EXISTS coffee_db.sales_order;
CREATE TABLE coffee_db.sales_order (order_number int PRIMARY KEY, item_name varchar(255) NOT NULL, item_type varchar(255) NOT NULL,
        salesman_number int NOT NULL, CONSTRAINT FK_sales_order FOREIGN KEY (salesman_number) REFERENCES salesman(salesman_number) ON DELETE CASCADE);