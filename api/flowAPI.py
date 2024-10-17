# URL - https://app.prefect.cloud/account/8ff8f613-92c4-44ce-b811-f9956023e78d/workspace/04d8fca9-df2e-40c8-ae4f-a3733114c475/dashboard

# URL - https://app.prefect.cloud/api/docs

import requests



# Replace these variables with your actual Prefect Cloud credentials
PREFECT_API_KEY = "pnu_FFykEnAJU012ye8VLAr2uqjWRN4BHZ0qyQvN"  # Your Prefect Cloud API key
ACCOUNT_ID = "667b13e3-f5e5-4cf0-b28f-0866a5cca958"  # Your Prefect Cloud Account ID
WORKSPACE_ID = "d36a4c31-f425-4967-a0e7-8dbe0ea9b332"  # Your Prefect Cloud Workspace ID
FLOW_ID="8c09285c-44b8-4c94-8cae-5fd807f3d494"

# Correct API URL to get flow details
PREFECT_API_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/flows/{FLOW_ID}"

# Set up headers with Authorization
headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}

# Make the request using GET
response = requests.get(PREFECT_API_URL, headers=headers)

print('Fetching @flow data from prefect cloud using rest API ')
# Check the response status
if response.status_code == 200:
    flow_info = response.json()
    print(flow_info)
else:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response content: {response.text}")
