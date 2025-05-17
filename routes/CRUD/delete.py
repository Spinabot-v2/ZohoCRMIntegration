from flask import Blueprint, jsonify, request
from token_handler.tokens import fetch_tokens
import requests
from utils.extension import limiter
from routes.zoho_constants import Constants
delete_blueprint = Blueprint("delete", __name__)

@delete_blueprint.route("/<int:remodel_id>/leads", methods=['DELETE'])
@limiter.limit("5 per minute")
def delete_clients(remodel_id):
    """
    Delete Leads in Zoho CRM.

    ---
    tags:
      - Leads
    parameters:
      - in: path
        name: remodel_id
        required: true
        schema:
          type: integer
        description: The ID of the remodel project.
      - in: query
        name: ids
        required: true
        schema:
          type: string
        description: Comma-separated list of lead IDs to delete (e.g., "id1,id2").
    responses:
      200:
        description: Leads deleted successfully.
      400:
        description: No lead IDs provided or invalid input.
      401:
        description: Unauthorized access.
      500:
        description: Internal server error.
    """
    
    ids = request.args.get("ids")
    if not ids:
        return jsonify({"error": "No lead IDs provided"}), 400

    try:
        token_data = fetch_tokens(remodel_id)
        if "error" in token_data:
            return jsonify(token_data), 401
        access_token = token_data.get("access_token")
        if not access_token:
            return jsonify({"error": "No access token_data found"}), 401
    except Exception as e:
        return jsonify({"error": "Failed to fetch access token_data", "details": str(e)}), 500

    zoho_url = Constants.ZOHO_API_URL
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    params = {"ids": ids}

    try:
        response = requests.delete(zoho_url, headers=headers, params=params)
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

