from dotenv import load_dotenv
import e2b
import openai
import asyncio
import json
import os

load_dotenv()

# Exporting session for external access
session: e2b.Session = None

# The OpenAI functions we want to use in our model.
functions = [
  {
      "name": "exec_code",
      "description": "Executes the passed Salesforce Apex code and returns the result.",
      "parameters": {
          "type": "object",
          "properties": {
              "code": {
                  "type": "string",
                  "description": "The Salesforce Apex code to execute.",
              },
          },
          "required": ["code"],
      },
  },
  {
    "name": "query_salesforce",
    "description": "Executes a SOQL query in Salesforce.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The SOQL query to execute.",
            },
        },
        "required": ["query"],
    },
  }
]

# Exporting run_code function for external access
async def run_code(code: str):
  global session
  # Get the Apex code file path from an environment variable, or use a default if not set
  apex_file_path = os.environ.get("APEX_FILE_PATH", "/home/user/index.apex")
  
  # 1. First we need to write the code to a file.
  await session.filesystem.write(apex_file_path, code)
  # 2. Then execute the file with Salesforce CLI.
  proc = await session.process.start(f"sfdx force:apex:execute -f {apex_file_path}")
  # 3. Wait for the process to finish.
  out = await proc
  # 4. Return the result.
  return out.stdout, out.stderr


async def parse_gpt_response(response):
  # Extracts the first message from GPT response
  message = response["choices"][0]["message"]
  if message.get("function_call"):
    func = message["function_call"]
    func_name = func["name"]

    # Get rid of newlines and leading/trailing spaces in the raw function arguments JSON string.
    # This sometimes help to avoid JSON parsing errors.
    args = func["arguments"].strip().replace("\n", "")
    # Parse the cleaned up JSON string.
    func_args = json.loads(args)

    # If the model is calling the exec_code function we defined in the `functions` variable, 
    # we want to save the `code` argument to a variable.
    if func_name == "exec_code":
      code = func_args["code"]
      stdout, stderr = await run_code(code)
      print(stdout)
      print(stderr)
    elif func_name == "query_salesforce":
      query = func_args["query"]
      print(stdout)
      print(stderr)
  else:
    # The model didn't call a function, so we just print the message.
    content = message["content"]
    print(content)

async def main():
  global session
  session = await e2b.Session.create(id="Salesforce")


  response = openai.ChatCompletion.create(
    model="gpt-4", # Or use "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "You are a senior developer that can code in Salesforce Apex. Always produce valid JSON."},
        {"role": "user", "content": "Create a new Account record"},
        {"role": "assistant", "content": '{"code": "Account acc = new Account(Name=\'Test Account\'); insert acc;"}', "name":"sharad_testing"},
        {"role": "user", "content": "Query all Account records"},
    ],
    functions=functions,
  )
  print(response)
  await parse_gpt_response(response)

asyncio.run(main())