from .database import execute_query, execute_read_query
from datetime import datetime

def calculate_total_cost(price_per_night, check_in, check_out):
    """Calculate total cost based on number of nights."""
    check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
    check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
    num_nights = (check_out_date - check_in_date).days
    return float(price_per_night) * num_nights, num_nights

def create_booking(user_id, room_id, check_in, check_out, price_per_night):
    """Create a new booking with payment."""
    total_cost, num_nights = calculate_total_cost(price_per_night, check_in, check_out)
    
    # Create booking
    booking_query = """
        INSERT INTO Booking (Total_cost, status, check_in_date, check_out_date, user_id, room_id)
        VALUES (%s, 'Pending', %s, %s, %s, %s)
    """
    
    if execute_query(booking_query, (total_cost, check_in, check_out, user_id, room_id)):
        # Get the last inserted booking_id
        booking_id_result = execute_read_query("SELECT LAST_INSERT_ID() as booking_id")
        if booking_id_result:
            booking_id = booking_id_result[0]['booking_id']
            
            # Create payment record
            payment_query = "INSERT INTO Payment (amount, booking_id) VALUES (%s, %s)"
            execute_query(payment_query, (total_cost, booking_id))
            
            return True, f"Booking created! Total: {total_cost:.2f} TK for {num_nights} night(s)", booking_id
    
    return False, "Failed to create booking.", None

def get_user_bookings(user_id):
    """Get all bookings for a specific user."""
    query = """
        SELECT b.*, r.description as room_description, r.price, r.image_url,
               l.city, l.area, p.amount as payment_amount
        FROM Booking b
        JOIN Room r ON b.room_id = r.Room_id
        LEFT JOIN Location l ON r.Postal_code = l.Postal_code
        LEFT JOIN Payment p ON b.booking_id = p.booking_id
        WHERE b.user_id = %s
        ORDER BY b.check_in_date DESC
    """
    return execute_read_query(query, (user_id,))

def get_all_bookings():
    """Get all bookings (admin view)."""
    query = """
        SELECT b.*, u.name as user_name, u.`e-mail` as user_email,
               r.description as room_description, r.price,
               l.city, l.area
        FROM Booking b
        JOIN USER u ON b.user_id = u.user_id
        JOIN Room r ON b.room_id = r.Room_id
        LEFT JOIN Location l ON r.Postal_code = l.Postal_code
        ORDER BY b.check_in_date DESC
    """
    return execute_read_query(query)

def update_booking_status(booking_id, new_status):
    """Update booking status (admin function)."""
    query = "UPDATE Booking SET status = %s WHERE booking_id = %s"
    if execute_query(query, (new_status, booking_id)):
        return True, f"Booking status updated to {new_status}"
    return False, "Failed to update booking status"

def get_booking_details(booking_id):
    """Get detailed information about a specific booking."""
    query = """
        SELECT b.*, r.description as room_description, r.price, r.image_url,
               l.city, l.area, p.amount as payment_amount
        FROM Booking b
        JOIN Room r ON b.room_id = r.Room_id
        LEFT JOIN Location l ON r.Postal_code = l.Postal_code
        LEFT JOIN Payment p ON b.booking_id = p.booking_id
        WHERE b.booking_id = %s
    """
    results = execute_read_query(query, (booking_id,))
    return results[0] if results else None
