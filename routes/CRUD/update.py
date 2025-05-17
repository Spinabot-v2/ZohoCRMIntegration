#in this we will create a route to update user infor based on his record id 
from flask import Blueprint 
from flask import request ,jsonify
from database.schemas import ZohoCreds
from routes.CRUD.clients import clients_blueprint
from token_handler.tokens import fetch_tokens
from database.insert_data_db import insert_audit_data
import requests
from utils.extension import limiter
from routes.zoho_constants import Constants
update_blueprint = Blueprint('update', __name__)
@clients_blueprint.route("/<int:remodel_id>/leads", methods=["PUT"])

@limiter.limit("5 per minute")
def update_clients(remodel_id):
    """
    Update Leads in Zoho CRM.

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
      - in: body
        name: body
        required: true
        description: JSON object containing lead data to update.
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "6707647000000775020"
                  Annual_Revenue:
                    type: integer
                    example: 1600000
                  City:
                    type: string
                    example: "Los Angeles Updated"
                  Company:
                    type: string
                    example: "Innovatech Solutions Updated"
                  Email:
                    type: string
                    example: "elon.musk.updated@example.com"
                  First_Name:
                    type: string
                    example: "Elon Updated"
                  Last_Name:
                    type: string
                    example: "Musk Updated"
                  Phone:
                    type: string
                    example: "555-555-9998"
                  Lead_Status:
                    type: string
                    example: "Contacted"
    responses:
      200:
        description: Leads updated successfully.
      400:
        description: Invalid input or missing required fields.
      401:
        description: Unauthorized access.
      500:
        description: Internal server error.
    """
    try:
        token_data = fetch_tokens(remodel_id)
        if "error" in token_data:
            return jsonify(token_data), 401
        access_token = token_data.get("access_token")
        if not access_token:
            return jsonify({"message": "User tokens not found. Please reauthorize."}), 401
    except Exception as e:
        return jsonify({"error": "token_data fetch failed", "details": str(e)}), 500

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    zoho_url = Constants.ZOHO_API_URL

    try:
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "Invalid JSON body"}), 400

        response = requests.put(zoho_url, json=data, headers=headers)

        try:
            res_json = response.json()
        except ValueError:
            return jsonify({"error": "Invalid response from Zoho"}), 502

        if response.status_code == 200:
            insert_audit_data(remodel_id,response.json(),mode="update")
            return jsonify(res_json), 200
        else:
            return jsonify({"status": "error", "message": "Error updating data", "details": res_json}), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": "Network error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500
