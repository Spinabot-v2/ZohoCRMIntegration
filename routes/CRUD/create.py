from flask import Blueprint, request, jsonify
import requests
from token_handler.tokens import fetch_tokens
from database.insert_data_db import insert_audit_data
from utils.extension import limiter
from routes.zoho_constants import Constants
create_blueprint = Blueprint("create", __name__)
@create_blueprint.route("/<int:remodel_id>/leads", methods=["POST"])
@limiter.limit("5 per minute")
def create_lead(remodel_id):
    """
    Create Leads in Zoho CRM.

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
        description: JSON object containing lead data.
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                example:  # Add the provided sample data here
                  {
                    "Annual_Revenue": 1000000,
                    "City": "New York",
                    "Company": "Tech Innovators",
                    "Country": "United States",
                    "Created_By": {
                      "email": "developer@spinabot.com",
                      "id": "6707647000000503001",
                      "name": "karhteek V"
                    },
                    "Created_Time": "2025-04-30T03:45:10-04:00",
                    "Email": "Bill.gates@example.com",
                    "First_Name": "BILL",
                    "Industry": "Technology",
                    "Last_Name": "Gates",
                    "Lead_Source": "Cold Call",
                    "Lead_Status": "New",
                    "Mobile": "555-555-7777",
                    "Modified_By": {
                      "email": "developer@spinabot.com",
                      "id": "6707647000000503001",
                      "name": "karhteek V"
                    },
                    "Modified_Time": "2025-04-30T03:45:10-04:00",
                    "No_of_Employees": 500,
                    "Owner": {
                      "email": "developer@spinabot.com",
                      "id": "6707647000000503001",
                      "name": "karhteek V"
                    },
                    "Phone": "555-555-7777",
                    "Rating": "A",
                    "Secondary_Email": "bgates@secondary.com",
                    "Skype_ID": "bgates",
                    "State": "CA",
                    "Street": "123 Innovation Blvd",
                    "Website": "http://www.techinnovators.com",
                    "Zip_Code": "12345",
                    "id": "6707647000000665004"
                  }
    responses:
      200:
        description: Leads created successfully.
      400:
        description: Invalid input or missing required fields.
      401:
        description: Unauthorized access.
      500:
        description: Internal server error.
    """
    try:
        zoho_url = Constants.ZOHO_API_URL
        try:
            request_body = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "Invalid JSON body"}), 400

        leads = request_body.get("data", [])
        layout_id = request_body.get("layout_id")  # optional

        if not leads:
            return jsonify({"error": "No leads provided"}), 400

        try:
            token_data = fetch_tokens(remodel_id)
            if "error" in token_data:
                return jsonify(token_data), 401
            access_token = token_data.get("access_token")
            if not access_token:
                return jsonify({"error": "Invalid or missing access token_data"}), 401
        except Exception as e:
            return jsonify({"error": "Failed to fetch token_data", "details": str(e)}), 500

        processed_leads = []
        for lead in leads:
            required_fields = ["First_Name", "Last_Name", "Company", "Email", "Phone"]# this is compulsary to this is a check point
            missing_fields = [field for field in required_fields if not lead.get(field)]
            if missing_fields:
                return jsonify({"error": f"Each lead must include {', '.join(missing_fields)}"}), 400

            if layout_id:
                lead["Layout"] = {"id": layout_id}

            clean_lead = {k: v for k, v in lead.items() if v is not None}
            processed_leads.append(clean_lead)

        payload = {
            "data": processed_leads,
            "trigger": ["workflow", "approval"]
        }

        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(zoho_url, json=payload, headers=headers)
        except requests.RequestException as e:
            return jsonify({"error": "Request to Zoho failed", "details": str(e)}), 502

        try:
            response_data = response.json()
        except ValueError:
            return jsonify({"error": "Invalid JSON response from Zoho"}), 502

        if response.status_code in [200, 201]:#success 
            insert_audit_data(remodel_id,response.json(),mode="create")
            return jsonify(response_data), response.status_code
        else:
            return jsonify({
                "error": "Zoho API request failed",
                "status_code": response.status_code,
                "details": response_data
            }), response.status_code

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
