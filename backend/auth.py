import bcrypt
from .database import execute_query, execute_read_query

def hash_password(password):
    """Hash a password for storing."""
    # salt = bcrypt.gensalt()
    # hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # return hashed.decode('utf-8')
    # Using a simpler approach for now to match common Python bcrypt usage, verifying compatibility
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def register_user(name, email, phone, password):
    """Register a new user."""
    # Check if user already exists
    users = execute_read_query("SELECT * FROM USER WHERE `e-mail` = %s", (email,))
    if users:
        return False, "User with this email already exists."

    hashed_password = hash_password(password)
    query = "INSERT INTO USER (name, `e-mail`, phone, password) VALUES (%s, %s, %s, %s)"
    params = (name, email, phone, hashed_password)
    
    if execute_query(query, params):
        return True, "Registration successful!"
    else:
        return False, "Registration failed."

def login_user(email, password):
    """Log in a user."""
    users = execute_read_query("SELECT * FROM USER WHERE `e-mail` = %s", (email,))
    if not users:
        return None, "Invalid email or password."
    
    user = users[0]
    if verify_password(user['password'], password):
        return user, "Login successful!"
    else:
        return None, "Invalid email or password."
