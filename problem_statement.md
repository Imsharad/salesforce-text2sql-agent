# Product Requirements Document

## Overview

The goal is to build an AI-powered chatbot application that can understand and respond to Salesforce-related questions in natural language, convert those responses into executable Salesforce Apex code, and run the generated code in a secure sandbox environment using the e2b service.

## User Stories

- As a user, I want to ask Salesforce-related questions in natural language and receive accurate responses.
- As a user, I want the chatbot to convert the natural language responses into functional Salesforce Apex code.
- As a user, I want the generated Apex code to be executed in a safe and isolated sandbox environment.

## Requirements

1. Integration with e2b Sandbox Service

   - The application must integrate with the e2b sandbox service to provide a secure code execution environment.
   - The e2b sandbox will be used to run the code interpreter for executing the generated Apex code.
2. Natural Language to Apex Code Conversion

   convert the natural language responses into valid and executable Salesforce Apex code.

   ##### Apex Code Execution in Sandbox
3. The application must utilize the e2b sandbox service to execute the generated Apex code securely.

## Acceptance Criteria

1. The chatbot successfully understands and responds to Salesforce-related questions in natural language.
2. The natural language responses are accurately converted into functional Salesforce Apex code.
3. The generated Apex code is executed successfully and safely within the e2b sandbox environment.
4. The application integrates seamlessly with the e2b sandbox service, following the provided documentation and guidelines.

## Constraints

- The e2b sandbox service's usage limits and restrictions must be taken into consideration.

## Assumptions

- The necessary Salesforce APIs and endpoints are accessible and properly configured.
- The e2b sandbox service is available and functioning as expected.

## Dependencies

- Integration with the e2b sandbox service for secure code execution.
- Access to Salesforce APIs and resources for retrieving and manipulating data.
- Availability of a large language model (AI/LLM) for natural language understanding and generation.
