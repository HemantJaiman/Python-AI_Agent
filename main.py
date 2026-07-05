from google.genai import client
import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import ollama

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


    ####### Chat with GEMINI ############
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    client = genai.Client(api_key=api_key)
    #model = "gemini-2.5-flash"
    model = "gemini-2.5-flash-lite"

    response = client.models.generate_content(
        model=model,
        contents=messages,
    )
    print(response.text)
    if verbose:
        print(f"user prompt: {user_prompt}")
        print(f"prompt tokens used: {response.usage_metadata.prompt_token_count}")
        print(f"response tokens used: {response.usage_metadata.candidates_token_count}")
        print(f"total tokens used: {response.usage_metadata.total_token_count}")


    

if __name__ == "__main__":
    main()