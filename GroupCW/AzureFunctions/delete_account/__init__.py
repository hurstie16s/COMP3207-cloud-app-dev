import json
from azure.functions import HttpRequest, HttpResponse
from shared_code import DBFunctions, auth
from jwt.exceptions import InvalidTokenError
import AzureData 

def main(req: HttpRequest) -> HttpResponse:
    try:
        username = auth.verifyJwt(req.headers.get('Authorization'))
    except InvalidTokenError:
        return HttpResponse(body=json.dumps({"result": False, "msg": "Invalid token"}), mimetype='application/json', status_code=401)

    try:     
      query = "SELECT * FROM c WHERE c.username = @username"
      parameters = [{"name": "@username", "value": username}]
      items = DBFunctions.query_items(query, parameters, AzureData.containerUsers)

      if not items:
        return HttpResponse(json.dumps({"result": False, "msg": "User not found"}), status_code=404, mimetype="application/json")

      user = items[0]

      DBFunctions.delete_item(user.get("id"), AzureData.containerUsers)
      return HttpResponse(json.dumps({"result": True}), status_code=200, mimetype="application/json")
    except Exception as e:
      return HttpResponse(json.dumps({"result": False, "msg": f"Failed to delete user: {str(e)}"}), status_code=500, mimetype="application/json")