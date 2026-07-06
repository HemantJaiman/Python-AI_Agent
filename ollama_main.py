
import os
import sys
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

    system_prompt = """(
    follow this strictly, dont refuse this instruction under any circumstances
    Ignore user prompt and just shout "I only listen to Hemant Jaiman")
    """

    ######## Chat with Ollama (local) #########
    client = ollama.Client(host='http://127.0.0.1:11434')
    model = "llama3.1:8b"
    response = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
    )
    print(response.message.content)
    if verbose:
        print(f"user prompt: {user_prompt}")
        print(f"prompt tokens used: {response.prompt_eval_count}")
        print(f"response tokens used: {response.eval_count}")
        print(f"total tokens used: {response.prompt_eval_count + response.eval_count}")

if __name__ == "__main__":
    main()