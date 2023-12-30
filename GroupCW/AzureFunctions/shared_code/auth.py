import jwt
import os

JWT_SIGNING_KEY = os.environ.get('JwtSigningKey')

def signJwt(username):
  return jwt.encode({"sub": username}, JWT_SIGNING_KEY, algorithm="HS256")

# Returns username
def verifyJwt(token) -> str:
  claims = jwt.decode(token, JWT_SIGNING_KEY, algorithms="HS256", options={"require": ["sub"]})
  return claims["sub"] # JWT decoding will throw an exception if the subject claim is missing