#System Imports
import bcrypt

# TODO: Password hashing
# TODO: Salt generation

def hash_password(password):
    # Generate salt to hash password with
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hash(password, salt)
    return hash_password

def verify(passwordToVerify, hashedPassword):
    return bcrypt.verify(passwordToVerify, hashedPassword)