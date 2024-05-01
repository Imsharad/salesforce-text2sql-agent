import openai
import json
from e2b import Sandbox, run_code
from simple_salesforce import Salesforce

def generate_apex_code(user_input):
    conversation = [
        {"role": "system", "content": "You are a Salesforce Apex code generator. Generate Apex code based on the user's intent."},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
        functions=[
            {
                "name": "generate_apex_code",
                "description": "Generates Salesforce Apex code based on the user's intent.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_input": {
                            "type": "string",
                            "description": "The user's intent or requirements for generating Apex code."
                        }
                    },
                    "required": ["user_input"]
                }
            }
        ]
    )

    function_call = response['choices'][0]['message']['function_call']
    function_name = function_call['name']
    function_args = function_call['arguments']

    if function_name == 'generate_apex_code':
        apex_code = json.loads(function_args)['apex_code']
        return apex_code
    else:
        return None

# Assuming your API key is 'your_api_key_here'
sandbox = Sandbox(template="base", api_key="e2b_983579084497a084ed8c04e6a8da3ec476235b26")


# add this to startup script everytime we instantiate the sandbox
# Replace notebook.exec_cell with run_code
stdout, stderr = run_code('Python3', '!pip install openai simple_salesforce')
print(stdout)
print(stderr)

openai.api_key = "sk-proj-EYAS7eOs1cDK4oXToqKKT3BlbkFJa3Uu4rFy3iVSbSIFxuO6"

# Salesforce credentials
username = "im.sharad.jain-qbye@force.com"
password = "Imsharad44!!"
security_token = "Z3rDf2ohkVN9RnBMzFu1X0HEK"

# Create Salesforce instance
sf = Salesforce(username=username, 
                password=password,
                security_token=security_token, 
                domain='drive-ruby-3898')

user_input = "Create a new account with details: Sharad Jain, sharad@gmail.com"

apex_code = generate_apex_code(user_input)

if apex_code:
    print("Generated Apex Code:")
    print(apex_code)

    # Execute Apex code
    result = sf.restful('tooling/executeAnonymous', method='POST', data={'anonymousBody': apex_code})

    # Handle the result
    if result.status_code == 200:
        print("Execution Result:")
        print(result.text)
    else:
        print("Execution failed with status code:", result.status_code)
else:
    print("Failed to generate Apex code.")

sandbox.close()