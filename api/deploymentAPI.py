# URL - https://app.prefect.cloud/account/8ff8f613-92c4-44ce-b811-f9956023e78d/workspace/04d8fca9-df2e-40c8-ae4f-a3733114c475/dashboard

# URL - https://app.prefect.cloud/api/docs

import requests

# Replace these variables with your actual Prefect Cloud credentials


# Replace these variables with your actual Prefect Cloud credentials
PREFECT_API_KEY = "pnu_FFykEnAJU012ye8VLAr2uqjWRN4BHZ0qyQvN"  # Your Prefect Cloud API key
ACCOUNT_ID = "667b13e3-f5e5-4cf0-b28f-0866a5cca958"  # Your Prefect Cloud Account ID
WORKSPACE_ID = "d36a4c31-f425-4967-a0e7-8dbe0ea9b332"  # Your Prefect Cloud Workspace ID
DEPLOYMENT_ID= "e635cf81-83fa-4177-bfd4-f15fdd4a2637"

# Correct API URL to get deployment details
PREFECT_API_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/deployments/{DEPLOYMENT_ID}"

# Set up headers with Authorization
headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}

# Make the request using GET
response = requests.get(PREFECT_API_URL, headers=headers)

print('Fetching @deployment data from prefect cloud using rest API ')
# Check the response status
if response.status_code == 200:
    deployment_info = response.json()
    print(deployment_info)
else:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response content: {response.text}")
