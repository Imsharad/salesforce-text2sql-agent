from simple_salesforce import Salesforce
import requests

# Function to get the Clientell token
def get_clientell_token():
    url = "https://rev-prod-k8s.clientellone.com/clientell/api/user/login"
    body = {
        "email": "ruthuparna@getclientell.com",
        "password": "Clientell@123"
    }
    response = requests.post(url, json=body)
    return response.json()['access_token']

# Function to get the Salesforce token
def get_salesforce_token(clientell_token):
    url = "https://rev-prod-k8s.clientellone.com/api/salesforce/getAccessToken"
    headers = {
        "Authorization": f"Token {clientell_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()['access_token']

# Main function to perform a Salesforce query
def main():
    clientell_token = get_clientell_token()
    salesforce_token = get_salesforce_token(clientell_token)
    
    sf = Salesforce(instance_url='https://clientell4-dev-ed.my.salesforce.com',
                    session_id=salesforce_token)
    
    # Simpler example query
    result = sf.query("SELECT Id, Name, Industry FROM Account ORDER BY CreatedDate DESC LIMIT 5")
    
    print("Query Result:")
    print("=" * 50)
    print(f"{'Account ID':<18} {'Name':<30} {'Industry':<20}")
    print("=" * 50)
    
    # Extracting details from the query result
    for record in result['records']:
        account_id = record['Id']
        account_name = record['Name']
        account_industry = record['Industry'] if record['Industry'] else 'N/A'
        print(f"{account_id:<18} {account_name:<30} {account_industry:<20}")

    print("=" * 50)

if __name__ == "__main__":
    main()




