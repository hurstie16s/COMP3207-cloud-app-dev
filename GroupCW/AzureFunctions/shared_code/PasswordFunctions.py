#System Imports
import bcrypt
import base64
import re

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return base64.b64encode(hashed_password).decode('utf-8')

def verify(passwordToVerify, hashedPassword):
    decoded_hashed_password = base64.b64decode(hashedPassword)
    return bcrypt.checkpw(passwordToVerify.encode('utf-8'), decoded_hashed_password)

# Helper function to validate password strength and provide reasons for invalidity
def validate_password(password):
    reasons = []
    if len(password) < 8:
        reasons.append("Password must be at least 8 characters long.")
    if not re.search("[0-9]", password):
        reasons.append("Password must contain at least one number.")
    if not re.search("[A-Za-z]", password):
        reasons.append("Password must contain at least one letter.")
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        reasons.append("Password must contain at least one special character.")
    return reasons