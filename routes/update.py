#in this we will create a route to update user infor based on his record id 
from flask import Blueprint 
from flask import request ,jsonify
from database.schemas import ZohoCreds
from routes.clients import clients_blueprint
from token_handler.tokens import fetch_tokens
from database.insert_data_db import insert_audit_data
import requests
from utils.extension import limiter
update_blueprint = Blueprint('update', __name__)
@clients_blueprint.route("/<int:remodel_id>/leads", methods=["PUT"])

@limiter.limit("5 per minute")
def update_clients(remodel_id):
    print("updating_clients")
    try:
        token = fetch_tokens(remodel_id)
        if "error" in token:
            return jsonify(token), 401
        access_token = token.get("access_token")
        if not access_token:
            return jsonify({"message": "User tokens not found. Please reauthorize."}), 401
    except Exception as e:
        return jsonify({"error": "Token fetch failed", "details": str(e)}), 500

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    url = "https://www.zohoapis.com/crm/v8/Leads"

    try:
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "Invalid JSON body"}), 400

        response = requests.put(url, json=data, headers=headers)

        try:
            res_json = response.json()
        except ValueError:
            return jsonify({"error": "Invalid response from Zoho"}), 502

        if response.status_code == 200:
            insert_audit_data(remodel_id,response.json(),mode="update")
            updates = response.json()["data"]
            for update in updates:
                print(type(update["details"]["Created_Time"]))
            return jsonify(res_json), 200
        else:
            return jsonify({"status": "error", "message": "Error updating data", "details": res_json}), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": "Network error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500
