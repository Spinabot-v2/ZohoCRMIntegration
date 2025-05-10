from flask import Blueprint
from flask import request, jsonify, redirect
from database.get_creds_db import get_zoho_creds
from database.schemas import ZohoCreds
clients_blueprint = Blueprint('clients',__name__)
from config import Config
import requests
from flask import current_app as app
from token_handler.tokens import fetch_tokens
from utils.extension import limiter
from utils.extension import redis_client 
import json 
@clients_blueprint.route("/<int:remodel_id>/leads", methods=["GET"])  
@limiter.limit("5 per minute")
def get_clients(remodel_id):
    print("Fetching clients...")
    try:
        token = fetch_tokens(remodel_id)
        if "error" in token:
            return jsonify(token), 401
        token = token.get("access_token")
        if not token:
            return jsonify({"error": "Access token not found"}), 401
    except Exception as e:
        return jsonify({"error": "Error while fetching access token", "details": str(e)}), 500

    headers = {"Authorization": "Zoho-oauthtoken " + token}
    url = (
            "https://www.zohoapis.com/crm/v8/Leads?"
            "fields=First_Name,Last_Name,Company,Lead_Source,Lead_Status,Industry,"
            "Annual_Revenue,Phone,Mobile,Email,Secondary_Email,Skype_ID,Website,Rating,"
            "No_of_Employees,Email_Opt_out,Street,City,State,Zip_Code,Country,Created_By,"
            "Modified_By,Created_Time,Modified_Time,Owner,Lead_Owner,Twitter,Secondary_URL,"
            "Address&sort_by=Created_Time&sort_order=desc&per_page=200&page=1"
    )

    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")

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
