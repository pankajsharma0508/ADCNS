# URL - https://app.prefect.cloud/account/8ff8f613-92c4-44ce-b811-f9956023e78d/workspace/04d8fca9-df2e-40c8-ae4f-a3733114c475/dashboard

# Ref - https://app.prefect.cloud/api/docs

import requests



# Replace these variables with your actual Prefect Cloud credentials
PREFECT_API_KEY = "pnu_FFykEnAJU012ye8VLAr2uqjWRN4BHZ0qyQvN"  # Your Prefect Cloud API key
ACCOUNT_ID = "667b13e3-f5e5-4cf0-b28f-0866a5cca958"  # Your Prefect Cloud Account ID
WORKSPACE_ID = "d36a4c31-f425-4967-a0e7-8dbe0ea9b332"  # Your Prefect Cloud Workspace ID

# Correct API URL to list flow runs
PREFECT_API_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}"

print(PREFECT_API_URL)

data = {
    "sort": "CREATED_DESC",
    "limit": 5,
    "artifacts": {
        "key": {
            "exists_": True
        }
    }
}

headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}
endpoint = f"{PREFECT_API_URL}/artifacts/filter"

response = requests.post(endpoint, headers=headers, json=data)
print (response)
for artifact in response.json():
    print(artifact)