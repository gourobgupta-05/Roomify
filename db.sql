-- setup_database.sql

-- Create the database
CREATE DATABASE IF NOT EXISTS airbnb_booking;
USE airbnb_booking;

-- 1. Create USER Table
CREATE TABLE IF NOT EXISTS USER (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    `e-mail` VARCHAR(100) NOT NULL UNIQUE, -- Note the backticks for special char in column name
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- 2. Create Admin Table
CREATE TABLE IF NOT EXISTS Admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- 3. Create Location Table
-- Postal_code is PK. 
CREATE TABLE IF NOT EXISTS Location (
    Postal_code VARCHAR(20) PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    area VARCHAR(100) NOT NULL
);

-- 4. Create Room Table
CREATE TABLE IF NOT EXISTS Room (
    Room_id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    Postal_code VARCHAR(20),
    admin_id INT,
    FOREIGN KEY (Postal_code) REFERENCES Location(Postal_code) ON DELETE SET NULL,
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id) ON DELETE CASCADE
);

-- 5. Booking Table (Extra from schema diagram)
CREATE TABLE IF NOT EXISTS Booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    Total_cost DECIMAL(10, 2),
    status VARCHAR(50) DEFAULT 'Pending',
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    user_id INT,
    room_id INT,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Room(Room_id) ON DELETE CASCADE
);

-- 6. Payment Table (Extra from schema diagram)
CREATE TABLE IF NOT EXISTS Payment (
    Payment_id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10, 2),
    booking_id INT,
    FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON DELETE CASCADE
);

-- Dummy Data for Location (so the dropdown isn't empty)
INSERT INTO Location (Postal_code, city, area) VALUES 
('10001', 'New York', 'Manhattan'),
('90210', 'Beverly Hills', 'Los Angeles'),
('EC1A 1BB', 'London', 'City of London')
ON DUPLICATE KEY UPDATE city=city;

-- Default Admin Account
-- Email: admin@roomify.com
-- Password: admin123
INSERT INTO Admin (name, email, password) VALUES 
('Roomify Admin', 'admin@roomify.com', '$2b$12$LiCXw5KTYCiImn7GgzZ8OOZyG4iMLP.AS6SOIo0v/MJ92k9ht9OE2') 
ON DUPLICATE KEY UPDATE email=email;
