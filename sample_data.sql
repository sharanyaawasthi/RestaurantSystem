-- Adding Sample Data to the Database
USE restaurant_db;

INSERT INTO Customers (full_name, email, phone_nb) VALUES
('Miley', 'mileysmiley@outlook.com', '5137564563'),
('Minnie', 'minmin@gmail.com', '5134532345'),
('Akshat', 'akshatt@yahoo.com', '5138675674');

INSERT INTO Addresses (customer_id, address_label, street_address, city, state, zip_code) VALUES
(1, 'Home', '143 Auburn Ave', 'Cincinnati', 'OH', '45219'),
(1, 'Work', '500 Riddle Rd', 'Cincinnati', 'OH', '45202'),
(2, 'Home', '456 Oak Tree Rd', 'Cincinnati', 'OH', '45220'),
(3, 'Office', '2980 Scioto Rd', 'Cincinnati', 'OH', '45219');

INSERT INTO Staff (full_name, staff_role) VALUES
('Ella Lee', 'Manager'),
('Mitch Boyd', 'Head Chef'),
('Ankit Sharma', 'Chef'),
('Alex Smith', 'Delivery Driver'),
('Simiya Hughes', 'Delivery Driver');

INSERT INTO MenuItems (item_name, category, price) VALUES
('Margherita Pizza', 'Main', 14.99),
('Alfredo Pasta', 'Main', 15.99),
('Lobster Rissoto', 'Main', 21.50),
('Garlic Grab Pasta', 'Main', 18.50),
('Garlic Knots', 'Appetizer', 5.99),
('Garlic Bread', 'Appetizer', 5.99),
('Chips & Dip', 'Appetizer', 3.99),
('French Fries', 'Appetizer', 1.99),
('Tiramisu', 'Dessert', 6.50),
('Chocolate Cake', 'Dessert', 4.50),
('Ice Cream', 'Dessert', 3.50);

INSERT INTO Orders (customer_id, address_id, staff_id, order_status) VALUES
(1, 1, 4, 'Out for Delivery'),
(2, 3, 2, 'Placed');

INSERT INTO OrderItems (order_id, item_id, quantity) VALUES
(1, 1, 1),
(1, 7, 2),
(2, 5, 3),
(2, 10, 1);