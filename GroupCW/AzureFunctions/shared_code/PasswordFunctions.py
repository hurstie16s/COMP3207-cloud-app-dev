#System Imports
import bcrypt
import base64

# TODO: Password hashing
# TODO: Salt generation

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return base64.b64encode(hashed_password).decode('utf-8')

def verify(passwordToVerify, hashedPassword):
    decoded_hashed_password = base64.b64decode(hashedPassword)
    return bcrypt.checkpw(passwordToVerify.encode('utf-8'), decoded_hashed_password)
