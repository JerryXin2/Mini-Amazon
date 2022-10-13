
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
--SELECT pg_catalog.setval('public.users_id_seq',
                         --(SELECT MAX(id)+1 FROM Users),
                         --false);
\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
                      
\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Product_Reviews FROM 'Product_Reviews.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Seller_Reviews FROM 'Seller_Reviews.csv' WITH DELIMITER ',' NULL '' CSV
