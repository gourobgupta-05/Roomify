#!/usr/bin/env python3
"""
Fix database schema - Check and add missing columns in Booking table
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

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
        return None

def fix_booking_schema():
    """Ensure Booking table has correct column names"""
    connection = create_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # Get all columns in Booking table
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'airbnb_booking' 
            AND TABLE_NAME = 'Booking'
        """)
        
        columns = [row[0] for row in cursor.fetchall()]
        print(f"📋 Current Booking table columns: {', '.join(columns)}")
        
        # Check if check_in_date exists, if not, it might be named differently
        if 'check_in_date' not in columns:
            print("⚠️  Column 'check_in_date' not found")
            # Let's recreate the column with correct name if it's missing
            # First, check if there's a similar column
            if 'checkin_date' in columns:
                print("📝 Renaming checkin_date to check_in_date...")
                cursor.execute("ALTER TABLE Booking CHANGE COLUMN checkin_date check_in_date DATE NOT NULL")
            elif 'Check_in_date' in columns:
                print("📝 Renaming Check_in_date to check_in_date...")
                cursor.execute("ALTER TABLE Booking CHANGE COLUMN Check_in_date check_in_date DATE NOT NULL")
            else:
                print("📝 Adding check_in_date column...")
                cursor.execute("ALTER TABLE Booking ADD COLUMN check_in_date DATE NOT NULL AFTER status")
            connection.commit()
            print("✓ check_in_date column fixed")
        else:
            print("✓ check_in_date column exists")
        
        # Check if check_out_date exists
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'airbnb_booking' 
            AND TABLE_NAME = 'Booking'
        """)
        columns = [row[0] for row in cursor.fetchall()]
        
        if 'check_out_date' not in columns:
            print("⚠️  Column 'check_out_date' not found")
            if 'checkout_date' in columns:
                print("📝 Renaming checkout_date to check_out_date...")
                cursor.execute("ALTER TABLE Booking CHANGE COLUMN checkout_date check_out_date DATE NOT NULL")
            elif 'Check_out_date' in columns:
                print("📝 Renaming Check_out_date to check_out_date...")
                cursor.execute("ALTER TABLE Booking CHANGE COLUMN Check_out_date check_out_date DATE NOT NULL")
            else:
                print("📝 Adding check_out_date column...")
                cursor.execute("ALTER TABLE Booking ADD COLUMN check_out_date DATE NOT NULL AFTER check_in_date")
            connection.commit()
            print("✓ check_out_date column fixed")
        else:
            print("✓ check_out_date column exists")
        
        cursor.close()
        connection.close()
        print("✓ Booking table schema check complete")
        
    except Error as e:
        print(f"✗ Error fixing schema: {e}")
        if connection:
            connection.close()

if __name__ == "__main__":
    print("🔧 Fixing Booking table schema...")
    fix_booking_schema()
