import e2b
import asyncio
import openai
from main import session, run_code, parse_gpt_response
from e2b_code_interpreter import CodeInterpreter

async def generate_and_execute_apex():
    # Hardcoded user input for creating a new Salesforce account
    user_input = "Create a new Account record"

    # Use GPT-4 to generate the Apex code
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior developer that can code in Salesforce Apex. Always produce valid JSON."},
            {"role": "user", "content": user_input},
        ],
        functions=[
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
            }
        ]
    )

    # Parse the response and execute the code
    apex_code = await parse_gpt_response(response)

    # Execute the generated Apex code using e2b_code_interpreter
    sandbox = CodeInterpreter.create()
    execution = sandbox.notebook.exec_cell(apex_code)
    if execution.success:
        print("Execution successful")
    else:
        print("Execution failed:", execution.error)

async def main():
    global session
    # Ensure the session is created
    if not session:
        session = await e2b.Session.create(id="Salesforce")
    
    await generate_and_execute_apex()

if __name__ == "__main__":
    asyncio.run(main())