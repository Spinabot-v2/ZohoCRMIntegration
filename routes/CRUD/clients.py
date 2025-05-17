from flask import Blueprint
from flask import  jsonify
clients_blueprint = Blueprint('clients',__name__)
import requests
from flask import current_app as app
from token_handler.tokens import fetch_tokens
from utils.extension import limiter
from routes.zoho_constants import Constants
@clients_blueprint.route("/<int:remodel_id>/leads", methods=["GET"])  
@limiter.limit("5 per minute")
def get_clients(remodel_id):
    """
    Fetch leads from Zoho CRM.

    ---
    tags:
      - Leads
    parameters:
      - in: path
        name: remodel_id
        required: true
        schema:
          type: integer
        description: Remodel ID used to fetch access token_data and Zoho leads.
    responses:
      200:
        description: Successful fetch of leads.
      401:
        description: Unauthorized or token_data issue.
      500:
        description: Internal server error.
      502:
        description: Invalid JSON response from Zoho.
    """
    try:
        token_data = fetch_tokens(remodel_id)
        if "error" in token_data:
            return jsonify(token_data), 401
        token_data = token_data.get("access_token")
        if not token_data:
            return jsonify({"error": "Access token_data not found"}), 401
    except Exception as e:
        return jsonify({"error": "Error while fetching access token_data", "details": str(e)}), 500

    headers = {"Authorization": "Zoho-oauthtoken " + token_data}
    url = Constants.zoho_get_leads_url # zoho api url for fetching leads
    try:
        response = requests.get(url, headers=headers)

        # Safely try parsing the JSON
        try:
            data = response.json()
        except ValueError:
            return jsonify({"error": "Invalid JSON response from Zoho"}), 502
        if response.status_code == 200:
            return jsonify(data)
        else:
            return jsonify({
                "error": "Failed to fetch clients",
                "status_code": response.status_code,
                "details": data
            }), response.status_code

    except requests.RequestException as e:
            return jsonify({
                "error": "Network error while accessing Zoho CRM",
                "details": str(e)
            }), 500
