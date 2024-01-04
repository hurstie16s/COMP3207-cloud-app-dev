import jwt

def signJwt(username):
  import AzureData
  return jwt.encode({"sub": username}, AzureData.JWT_SIGNING_KEY, algorithm="HS256")

# Returns username
def verifyJwt(token) -> str:
  import AzureData
  claims = jwt.decode(token, AzureData.JWT_SIGNING_KEY, algorithms="HS256", options={"require": ["sub"]})
  return claims["sub"] # JWT decoding will throw an exception if the subject claim is missing