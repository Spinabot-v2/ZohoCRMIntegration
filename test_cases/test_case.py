import json
import requests

BASE_URL = "http://localhost:5000/api/clients/1/leads"
created_ids = []
def test_0_read_data():
    url = "http://localhost:5000/api/clients/1/leads"
    response = requests.get(url)

    # Check if the status is OK
    assert response.status_code == 200

    # Check if 'data' is in the response JSON
    json_data = response.json()
    assert "data" in json_data

    # Optionally check if it's a list or has expected keys
    assert isinstance(json_data["data"], list)

def test_1_create_lead():
    with open("test_cases/data/sample_data.json") as f:
        payload = json.load(f)

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201

    response_data = response.json()
    assert "data" in response_data

    # Save created IDs
    for record in response_data["data"]:
        assert record["code"] == "SUCCESS"
        created_ids.append(record["details"]["id"])

    assert len(created_ids) == len(payload["data"])


def test_2_update_lead():
    with open("test_cases/data/updated_data.json") as f:
        updated_payload = json.load(f)

    # Update IDs in the payload to match the ones just created
    for i, record in enumerate(updated_payload["data"]):
        record["id"] = created_ids[i]

    response = requests.put(BASE_URL, json=updated_payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "data" in response_data
    for record in response_data["data"]:
        assert record["code"] == "SUCCESS"
        assert record["message"] == "record updated"
        assert record["status"] == "success"


def test_3_delete_lead():
    ids_str = ",".join(created_ids)
    delete_url = f"{BASE_URL}?ids={ids_str}"

    response = requests.delete(delete_url)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["status"] == "success"
    for record in response_data["response"]["data"]:
        assert record["code"] == "SUCCESS"
        assert record["message"] == "record deleted"
        assert record["status"] == "success"
