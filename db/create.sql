-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Sellers;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Carts;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Product_Reviews;
DROP TABLE IF EXISTS Seller_Reviews;

CREATE TABLE Users (
    uid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR (255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    balance DECIMAL(12,2) NOT NULL DEFAULT 0
);

CREATE TABLE Sellers(
    uid INT NOT NULL PRIMARY KEY REFERENCES Users(uid),
    seller VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    product_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    seller_id INT NOT NULL REFERENCES Sellers(uid),
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    description VARCHAR(65535) NOT NULL,
    image VARCHAR(4095) NOT NULL, --url of image
    price DECIMAL(12,2) NOT NULL CHECK (price > 0),
    available BOOLEAN DEFAULT TRUE,
    quantity INT NOT NULL CHECK (quantity >= 0)
);

CREATE TABLE Carts (
    uid INT NOT NULL REFERENCES Users(uid),
    product_id INT NOT NULL REFERENCES Products(product_id),
    quantity INT NOT NULL,  
    PRIMARY KEY(uid, product_id)
);

CREATE TABLE Orders(
    order_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    product_id INT NOT NULL REFERENCES Products(product_id),
    seller_id INT NOT NULL REFERENCES Sellers(uid),
    uid INT NOT NULL REFERENCES Users(uid),
    address VARCHAR(255) NOT NULL,
    order_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),    
    quantity INT NOT NULL,
    fulfillment BOOLEAN DEFAULT FALSE,
    fulfillment_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    price DECIMAL(12, 2) NOT NULL CHECK (price > 0)
);

CREATE TABLE Product_Reviews(
    product_id INT NOT NULL REFERENCES Products(product_id),
    uid INT NOT NULL REFERENCES Users(uid),
    review VARCHAR(65535) NOT NULL,
    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    PRIMARY KEY(uid, product_id)
);

CREATE TABLE Seller_Reviews(
    seller_id INT NOT NULL REFERENCES Sellers(uid),
    reviewer_id INT NOT NULL REFERENCES Users(uid),
    review VARCHAR(65535) NOT NULL,
    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    PRIMARY KEY(reviewer_id, seller_id)
);

