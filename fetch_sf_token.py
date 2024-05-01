import requests

# Step 1: Login to Clientell API
login_url = "https://rev-prod-k8s.clientellone.com/clientell/api/user/login"
login_data = {"email": "ruthuparna@getclientell.com", "password": "Clientell@123"}
response = requests.post(login_url, json=login_data)
clientell_token = response.json()['access_token']
print("Clientell Token:", clientell_token)  # Print Clientell token

# Step 2: Get Salesforce Token
salesforce_token_url = "https://rev-prod-k8s.clientellone.com/api/salesforce/getAccessToken"
headers = {"Authorization": f"Token {clientell_token}"}
response = requests.get(salesforce_token_url, headers=headers)
salesforce_token = response.json()['access_token']
print("Salesforce Token:", salesforce_token)  # Print Salesforce token

# Now you can use `salesforce_token` to make Salesforce API calls.