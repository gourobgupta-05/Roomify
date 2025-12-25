#!/usr/bin/env python3
"""
Sample Data Population Script for Roomify
This script populates the database with realistic sample data for testing purposes.
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import bcrypt

# Load environment variables
load_dotenv()

def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'airbnb_booking')
        )
        if connection.is_connected():
            print("✓ Connected to MySQL database")
            return connection
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        sys.exit(1)
    return None

def clear_existing_data(cursor):
    """Clear existing sample data (optional - keeps admin account)."""
    try:
        print("\n📋 Clearing existing sample data...")
        # Delete in reverse order of foreign key dependencies
        cursor.execute("DELETE FROM Payment WHERE booking_id > 0")
        cursor.execute("DELETE FROM Booking WHERE booking_id > 0")
        cursor.execute("DELETE FROM Room WHERE Room_id > 0")
        cursor.execute("DELETE FROM USER WHERE user_id > 0")
        # Clear all locations to ensure we only have Bangladesh ones
        cursor.execute("DELETE FROM Location")
        # Clear admin to ensure we re-create with correct password hash
        cursor.execute("DELETE FROM Admin")
        print("✓ Cleared existing sample data")
    except Error as e:
        print(f"✗ Error clearing data: {e}")

def populate_locations(cursor):
    """Populate Location table with Bangladesh locations."""
    print("\n📍 Adding Bangladesh locations...")
    locations = [
        ('1212', 'Dhaka', 'Gulshan'),
        ('1209', 'Dhaka', 'Dhanmondi'),
        ('1213', 'Dhaka', 'Banani'),
        ('1230', 'Dhaka', 'Uttara'),
        ('1205', 'Dhaka', 'Elephant Road'),
        ('1216', 'Dhaka', 'Mirpur'),
        ('4000', 'Chittagong', 'Khulshi'),
        ('4100', 'Chittagong', 'Agrabad'),
        ('4203', 'Chittagong', 'Nasirabad'),
        ('3100', 'Sylhet', 'Zindabazar'),
        ('3101', 'Sylhet', 'Amberkhana'),
        ('2700', 'Cox\'s Bazar', 'Kolatoli'),
        ('2702', 'Cox\'s Bazar', 'Sugandha Beach'),
        ('6000', 'Rajshahi', 'Kazla'),
        ('9000', 'Khulna', 'Sonadanga'),
    ]
    
    query = """
        INSERT INTO Location (Postal_code, city, area) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE city=city
    """
    
    count = 0
    for location in locations:
        try:
            cursor.execute(query, location)
            count += 1
        except Error as e:
            print(f"  Warning: Location {location[1]}, {location[2]} might already exist")
    
    print(f"✓ Added {count} Bangladesh locations")

def populate_admin(cursor):
    """Populate Admin table with correct password hash."""
    print("\n👨‍💼 Adding Admin account...")
    # Properly hash the password using the script's function which uses the current bcrypt
    hashed_password = hash_password("admin123")
    
    query = """
        INSERT INTO Admin (name, email, password) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE password=%s
    """
    
    try:
        cursor.execute(query, ('Roomify Admin', 'admin@roomify.com', hashed_password, hashed_password))
        print("✓ Admin account created/updated with correct password hash")
    except Error as e:
        print(f"✗ Error creating admin: {e}")

def populate_users(cursor):
    """Populate USER table with sample users."""
    print("\n👥 Adding sample users...")
    
    # Password for all sample users: "password123"
    hashed_password = hash_password("password123")
    
    users = [
        ('Rahim Uddin', 'rahim@email.com', '+880-1711-123456', hashed_password),
        ('Karim Ahmed', 'karim@email.com', '+880-1811-654321', hashed_password),
        ('Ayesha Khan', 'ayesha@email.com', '+880-1911-987654', hashed_password),
        ('Fatima Begum', 'fatima@email.com', '+880-1611-456789', hashed_password),
        ('Tanvir Hasan', 'tanvir@email.com', '+880-1511-112233', hashed_password),
        ('Nusrat Jahan', 'nusrat@email.com', '+880-1311-334455', hashed_password),
        ('Sajid Rahman', 'sajid@email.com', '+880-1722-556677', hashed_password),
    ]
    
    query = """
        INSERT INTO USER (name, `e-mail`, phone, password) 
        VALUES (%s, %s, %s, %s)
    """
    
    count = 0
    for user in users:
        try:
            cursor.execute(query, user)
            count += 1
        except Error as e:
            print(f"  Warning: User {user[1]} might already exist")
    
    print(f"✓ Added {count} sample users")
    print(f"  📝 All users can login with password: password123")

def populate_rooms(cursor):
    """Populate Room table with diverse Bangladesh rooms."""
    print("\n🏠 Adding sample rooms...")
    
    # Get admin_id
    cursor.execute("SELECT admin_id FROM Admin LIMIT 1")
    result = cursor.fetchone()
    admin_id = result[0] if result else 1
    
    rooms = [
        # Dhaka rooms
        (5500.00, 'Luxury Apartment in Gulshan with Lake View', 
         'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800', '1212', admin_id),
        (4200.00, 'Cozy Flat in Dhanmondi near Rabindra Sarobar', 
         'https://images.unsplash.com/photo-1502672260066-6bc35f0a1611?w=800', '1209', admin_id),
        (6000.00, 'Modern Office/Studio in Banani', 
         'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800', '1213', admin_id),
        (3500.00, 'Spacious Family Apartment in Uttara', 
         'https://images.unsplash.com/photo-1549638441-b787d2e11f14?w=800', '1230', admin_id),
        
        # Chittagong rooms
        (4500.00, 'Hillside Villa in Khulshi', 
         'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800', '4000', admin_id),
        (3000.00, 'Convenient Apartment in Agrabad', 
         'https://images.unsplash.com/photo-1568495248636-6432b97bd949?w=800', '4100', admin_id),
        
        # Sylhet rooms
        (3800.00, 'Tea Garden View Suite in Sylhet', 
         'https://images.unsplash.com/photo-1571508601793-a9de1d4d28c9?w=800', '3100', admin_id),
        (2500.00, 'Affordable Room in Amberkhana', 
         'https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800', '3101', admin_id),
        
        # Cox's Bazar rooms
        (8500.00, 'Beachfront Penthouse in Kolatoli', 
         'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800', '2700', admin_id),
        (6500.00, 'Sea View Suite near Sugandha Beach', 
         'https://images.unsplash.com/photo-1494526585095-c41746248156?w=800', '2702', admin_id),
        
        # Other locations
        (2800.00, 'Quiet House in Rajshahi near University', 
         'https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800', '6000', admin_id),
        (2200.00, 'Comfortable Home in Khulna', 
         'https://images.unsplash.com/photo-1464146072230-91cabc968266?w=800', '9000', admin_id),
    ]
    
    query = """
        INSERT INTO Room (price, description, image_url, Postal_code, admin_id) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    count = 0
    for room in rooms:
        try:
            cursor.execute(query, room)
            count += 1
        except Error as e:
            print(f"  Error adding room: {e}")
    
    print(f"✓ Added {count} sample rooms")

def populate_bookings(cursor):
    """Populate Booking and Payment tables with sample data."""
    print("\n📅 Adding sample bookings...")
    
    # Get user IDs
    cursor.execute("SELECT user_id FROM USER")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    # Get room IDs
    cursor.execute("SELECT Room_id, price FROM Room")
    rooms = cursor.fetchall()
    
    if not user_ids or not rooms:
        print("  ⚠ No users or rooms found. Skipping bookings.")
        return
    
    # Create bookings with different statuses and dates
    today = datetime.now().date()
    
    bookings = [
        # Past bookings (Completed)
        (user_ids[0], rooms[0][0], today - timedelta(days=30), today - timedelta(days=25), 
         rooms[0][1] * 5, 'Completed'),
        (user_ids[1], rooms[2][0], today - timedelta(days=20), today - timedelta(days=17), 
         rooms[2][1] * 3, 'Completed'),
        
        # Current bookings (Confirmed)
        (user_ids[2], rooms[4][0], today - timedelta(days=2), today + timedelta(days=3), 
         rooms[4][1] * 5, 'Confirmed'),
        (user_ids[3], rooms[6][0], today, today + timedelta(days=7), 
         rooms[6][1] * 7, 'Confirmed'),
        
        # Future bookings (Pending)
        (user_ids[0], rooms[8][0], today + timedelta(days=10), today + timedelta(days=15), 
         rooms[8][1] * 5, 'Pending'),
        (user_ids[1], rooms[10][0], today + timedelta(days=20), today + timedelta(days=25), 
         rooms[10][1] * 5, 'Pending'),
        (user_ids[4], rooms[1][0], today + timedelta(days=15), today + timedelta(days=18), 
         rooms[1][1] * 3, 'Confirmed'),
        
        # Cancelled bookings
        (user_ids[5], rooms[11][0], today + timedelta(days=30), today + timedelta(days=35), 
         rooms[11][1] * 5, 'Cancelled'),
        
        # More diverse bookings
        (user_ids[2], rooms[3][0], today + timedelta(days=45), today + timedelta(days=50), 
         rooms[3][1] * 5, 'Pending'),
        (user_ids[3], rooms[5][0], today - timedelta(days=10), today - timedelta(days=7), 
         rooms[5][1] * 3, 'Completed'),
    ]
    
    booking_query = """
        INSERT INTO Booking (user_id, room_id, check_in_date, check_out_date, Total_cost, status) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    payment_query = """
        INSERT INTO Payment (amount, booking_id) 
        VALUES (%s, %s)
    """
    
    count = 0
    for booking in bookings:
        try:
            cursor.execute(booking_query, booking)
            booking_id = cursor.lastrowid
            
            # Create corresponding payment
            cursor.execute(payment_query, (booking[4], booking_id))
            count += 1
        except Error as e:
            print(f"  Error adding booking: {e}")
    
    print(f"✓ Added {count} sample bookings with payments")

def main():
    """Main function to populate all sample data."""
    print("=" * 60)
    print("🚀 ROOMIFY - Sample Data Population Script")
    print("=" * 60)
    
    connection = create_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # Ask user if they want to clear existing data
        response = input("\n⚠️  Clear existing sample data first? (y/n): ").lower()
        if response == 'y':
            clear_existing_data(cursor)
        
        # Populate all tables
        populate_locations(cursor)
        populate_admin(cursor)
        populate_users(cursor)
        populate_rooms(cursor)
        populate_bookings(cursor)
        
        # Commit all changes
        connection.commit()
        
        # Show summary
        print("\n" + "=" * 60)
        print("✅ SAMPLE DATA POPULATION COMPLETED!")
        print("=" * 60)
        
        # Display counts
        cursor.execute("SELECT COUNT(*) FROM Location")
        print(f"📍 Total Locations: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM USER")
        print(f"👥 Total Users: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Admin")
        print(f"👨‍💼 Total Admins: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Room")
        print(f"🏠 Total Rooms: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Booking")
        print(f"📅 Total Bookings: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM Payment")
        print(f"💳 Total Payments: {cursor.fetchone()[0]}")
        
        print("\n📝 Sample Login Credentials:")
        print("   Admin: admin@roomify.com / admin123")
        print("   Users: john.doe@email.com / password123")
        print("          jane.smith@email.com / password123")
        print("          ahmed.rahman@email.com / password123")
        print("          (and more...)")
        
        print("\n🎉 You can now run the application and test all features!")
        print("   Run: python main.py")
        print("=" * 60)
        
    except Error as e:
        print(f"\n✗ Error during data population: {e}")
        connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\n✓ Database connection closed")

if __name__ == "__main__":
    main()
