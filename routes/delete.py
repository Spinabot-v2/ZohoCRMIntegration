from flask import Blueprint, jsonify, request
from token_handler.tokens import fetch_tokens
import requests
from utils.extension import limiter

delete_blueprint = Blueprint("delete", __name__)

@delete_blueprint.route("/<int:remodel_id>/leads", methods=['DELETE'])
@limiter.limit("5 per minute")
def delete_clients(remodel_id):
    print("Deleting Clients")
    
    ids = request.args.get("ids")
    if not ids:
        return jsonify({"error": "No lead IDs provided"}), 400

    try:
        token = fetch_tokens(remodel_id)
        if "error" in token:
            return jsonify(token), 401
        access_token = token.get("access_token")
        if not access_token:
            return jsonify({"error": "No access token found"}), 401
    except Exception as e:
        return jsonify({"error": "Failed to fetch access token", "details": str(e)}), 500

    url = "https://www.zohoapis.com/crm/v8/Leads"
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    params = {"ids": ids}

    try:
        response = requests.delete(url, headers=headers, params=params)
        try:
            res_json = response.json()
        except ValueError:
            res_json = {"message": "No JSON response from Zoho"}
        
        return jsonify({
            "status": "success" if response.status_code == 200 else "failure",
            "response": res_json
        }), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": "Network error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500

