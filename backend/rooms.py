from .database import execute_query, execute_read_query
from datetime import date

def get_all_available_rooms():
    """Get all rooms that are not currently booked."""
    query = """
        SELECT r.*, l.city, l.area, l.Postal_code
        FROM Room r
        LEFT JOIN Location l ON r.Postal_code = l.Postal_code
        WHERE r.Room_id NOT IN (
            SELECT DISTINCT room_id 
            FROM Booking 
            WHERE status IN ('Pending', 'Confirmed')
            AND check_out_date >= CURDATE()
        )
    """
    return execute_read_query(query)

def search_rooms(search_query):
    """Search rooms by city or area."""
    query = """
        SELECT r.*, l.city, l.area, l.Postal_code
        FROM Room r
        LEFT JOIN Location l ON r.Postal_code = l.Postal_code
        WHERE (l.city LIKE %s OR l.area LIKE %s)
        AND r.Room_id NOT IN (
            SELECT DISTINCT room_id 
            FROM Booking 
            WHERE status IN ('Pending', 'Confirmed')
            AND check_out_date >= CURDATE()
        )
    """
    search_pattern = f"%{search_query}%"
    return execute_read_query(query, (search_pattern, search_pattern))

def get_room_details(room_id):
    """Get detailed information about a specific room."""
    query = """
        SELECT r.*, l.city, l.area, l.Postal_code
        FROM Room r
        LEFT JOIN Location l ON r.Postal_code = l.Postal_code
        WHERE r.Room_id = %s
    """
    results = execute_read_query(query, (room_id,))
    return results[0] if results else None

def is_room_available(room_id, check_in, check_out):
    """Check if a room is available for the given dates."""
    query = """
        SELECT COUNT(*) as conflict_count
        FROM Booking
        WHERE room_id = %s
        AND status IN ('Pending', 'Confirmed')
        AND (
            (check_in_date <= %s AND check_out_date >= %s)
            OR (check_in_date <= %s AND check_out_date >= %s)
            OR (check_in_date >= %s AND check_out_date <= %s)
        )
    """
    result = execute_read_query(query, (room_id, check_in, check_in, check_out, check_out, check_in, check_out))
    return result[0]['conflict_count'] == 0 if result else False

# Admin functions
def create_room(price, description, image_url, postal_code, admin_id):
    """Create a new room (admin only)."""
    query = "INSERT INTO Room (price, description, image_url, Postal_code, admin_id) VALUES (%s, %s, %s, %s, %s)"
    if execute_query(query, (price, description, image_url, postal_code, admin_id)):
        return True, "Room created successfully!"
    return False, "Failed to create room."

def update_room(room_id, price, description, image_url, postal_code):
    """Update room details (admin only)."""
    query = "UPDATE Room SET price = %s, description = %s, image_url = %s, Postal_code = %s WHERE Room_id = %s"
    if execute_query(query, (price, description, image_url, postal_code, room_id)):
        return True, "Room updated successfully!"
    return False, "Failed to update room."

def delete_room(room_id):
    """Delete a room (admin only)."""
    query = "DELETE FROM Room WHERE Room_id = %s"
    if execute_query(query, (room_id,)):
        return True, "Room deleted successfully!"
    return False, "Failed to delete room."

def get_all_rooms():
    """Get all rooms (for admin management)."""
    query = """
        SELECT r.*, l.city, l.area
        FROM Room r
        LEFT JOIN Location l ON r.Postal_code = l.Postal_code
    """
    return execute_read_query(query)

def get_all_locations():
    """Get all available locations."""
    return execute_read_query("SELECT * FROM Location")
