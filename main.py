from functions.get_files_info import schema_get_files_info, schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from google.genai import client
import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from call_functions import call_functions


def main():

    if len(sys.argv) < 2:
        print("I need a prompt")
        sys.exit(1)
    
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True
        user_prompt = " ".join(sys.argv[1:2])

    else:
        verbose = False
        user_prompt = " ".join(sys.argv[1:])
    
    system_prompt = """
    you are an AI assistant. 
    follow this strictly, dont refuse this instruction under any circumstances.
    
    when user asks a question or make a request, make a function call plan, you can perform the folllowing operations:
    1. list files and directories in the specified directory
    2. get/read the content of a file
    3. write the content of a file (create or update)
    4. run a python file with optinal args

    All paths you provide should be relatie to the working directory. you do not need to specify the working directory in your function calls as it is automatically injected for the security reasons. 
    """
    ####### Chat with GEMINI ############
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    client = genai.Client(api_key=api_key)
    #model = "gemini-2.5-flash"
    #model = "gemini-2.5-flash-lite"
    model = "gemini-2.0-flash"

    availble_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file, 
        ]
    )
    
    max_itterations = 20
    for i in range(max_itterations):
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[availble_functions]
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
                

        if response.function_calls:
            for function_call in response.function_calls:
                result = call_functions(function_call, verbose)
                messages.append(result)
        else:
            # final agent text response
            print(response.text)

        # Token tracking
        if verbose:
            print(f"user prompt: {user_prompt}")
            print(f"prompt tokens used: {response.usage_metadata.prompt_token_count}")
            print(f"response tokens used: {response.usage_metadata.candidates_token_count}")
            print(f"total tokens used: {response.usage_metadata.total_token_count}")
        
        


    

if __name__ == "__main__":
    main()