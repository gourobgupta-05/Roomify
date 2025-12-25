# Roomify - Airbnb Clone

Roomify is a room booking system similar to Airbnb.

## Prerequisites

- Python 3.x
- MySQL (XAMPP recommended)

### Database Setup

1. Start Apache and MySQL in XAMPP.
2. Go to `http://localhost/phpmyadmin`.
3. Create a database named `airbnb_booking` (or just import the SQL file).
4. Import `db.sql` into the `airbnb_booking` database.

## Setup Instructions

### macOS / Linux

1. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   ```
2. **Activate Virtual Environment:**
   ```bash
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application:**
   ```bash
   python3 main.py
   ```

### Windows

1. **Create Virtual Environment:**
   ```powershell
   python -m venv venv
   ```
2. **Activate Virtual Environment:**
   ```powershell
   .\venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run the Application:**
   ```powershell
   python main.py
   ```

## Usage

- Open your browser and navigate to the address shown in the terminal (usually `http://localhost:8080`).
- Use the **Sign Up** tab to create a new account.
- Use the **Login** tab to access the dashboard.

### Admin Access

- **Email**: `admin@roomify.com`
- **Password**: `admin123`

## Features

1. **User Registration & Login** - Secure signup with password hashing
2. **Browse Rooms** - View all available rooms with images and details
3. **Search** - Find rooms by city or area
4. **Book Room** - Select dates, view cost, confirm booking with payment popup
5. **My Bookings** - View booking history and status
6. **Admin Dashboard** - Manage rooms and bookings
