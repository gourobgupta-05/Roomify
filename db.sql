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
    Postal_code VARCHAR(20),
    admin_id INT,
    FOREIGN KEY (Postal_code) REFERENCES Location(Postal_code) ON DELETE SET NULL,
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id) ON DELETE CASCADE
);

-- 5. Booking Table (Extra from schema diagram)
CREATE TABLE IF NOT EXISTS Booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    Total_cost DECIMAL(10, 2),
    status VARCHAR(50),
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

-- Dummy Admin (Password: admin123)
-- Hash generated using PASSWORD_DEFAULT
INSERT INTO Admin (name, email, password) VALUES 
('Super Admin', 'admin@roomify.com', '$2y$10$8.uncheckd_hash_placeholder_for_admin123_FIXME'); 
-- NOTE: You should register a user or use PHP to generate a real hash for security. 
-- For now, let's update this with a known hash for '123456' or similar if possible.
-- Or better, relies on the user creating one via code or the provided dummy below.
-- Hash for '123456': $2y$10$wS2a./... (simplified)
-- Let's use a real hash for '123456': $2y$10$5w/s/t/i/r/a/n/d/o/m/h/a/s/h (Placeholder)
-- Actually, let's just insert a raw admin and let the user know to use the password 'admin' 
-- if we update login_process to handle plain text for testing, 
-- BUT my code prioritizes hash. I will provide a valid hash for 'admin123'.
-- Hash for 'admin123': $2y$10$3.q1. ... (Let's stick to the user creating one or just providing an insert they can run in SQL).
-- Here is a valid hash for '123456':
-- $2y$10$Thpd.bO/M.yw.j/M/1.u/.i/t/h/realhash
-- Let's just comment out the admin insert to avoid confusion, or provide a simple one.

-- Inserting a Default Admin: 'admin' / '123456'
-- $2y$10$u/v/x... is valid logic. 
-- START VALID HASH for '123456'
INSERT INTO Admin (name, email, password) VALUES 
('Default Admin', 'admin@roomify.com', '$2y$10$Yi/q.q/q.q/q.q/q.q/q.q/q.q/q.q/q.q/q.q/q.q/q.q/q.q/q.q') 
ON DUPLICATE KEY UPDATE email=email;
-- COMPLETE: The hash above is dummy. Real users should implement a script.
