import os
import sys
import ollama
import json
from functions.get_files_info import get_files_info as original_get_files_info
from functions.get_file_content import get_file_content as original_get_file_content
from functions.write_file import write_file as original_write_file
from functions.run_python_file import run_python_file as original_run_python_file

working_directory = "calculator"

def get_files_info(directory: str = ".") -> str:
    """lists files and directories in the specified directory along with file sizes.
    
    Args:
        directory: this directory to list files from, relative to working directory.if not provided, lists files in the working directory itself
    """
    return original_get_files_info(working_directory, directory)

def get_file_content(file_path: str) -> str:
    """get the content of the given file as a string, contrained to the working directory.
    
    Args:
        file_path: path to the file, relative to working directory
    """
    return original_get_file_content(working_directory, file_path)

def write_file(file_path: str, content: str) -> str:
    """writes the given content to a file at the specified file path. Creates the file and parent directories if they do not exist.
    
    Args:
        file_path: the path to the file to write, relative to the working directory
        content: the content to write to the file
    """
    return original_write_file(working_directory, file_path, content)

def run_python_file(file_path: str, cli_args: list[str] = None, **kwargs) -> str:
    """runs a python file and returns its output. accepts addition cli args as an optional array.
    
    Args:
        file_path: path to the python file to run, relative to working directory
        cli_args: array of strings representing the cli arguments to pass to the python script
    """
    args = cli_args
    if args is None:
        args = kwargs.get('args', [])
        
    if args is None:
        args = []
    elif isinstance(args, str):
        try:
            parsed = json.loads(args)
            if isinstance(parsed, list):
                args = [str(x) for x in parsed]
            else:
                args = [str(parsed)]
        except Exception:
            args = args.split()
    elif isinstance(args, list):
        args = [str(x) for x in args]
    else:
        args = [str(args)]
        
    return original_run_python_file(working_directory, file_path, args)

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
    
    You have access to the following tools:
    1. get_files_info: Lists files and directories in the specified directory along with file sizes.
    2. get_file_content: Reads the content of a file.
    3. write_file: Writes content to a file (creates/updates).
    4. run_python_file: Runs a python file with optional arguments.

    when user asking about any code related stuff then you should always refer to working directory's files and structure. you should not assume anything beyond the working directory.

    CRITICAL RULES:
    - You do not know what files are in the working directory at the beginning of the conversation. Therefore, you MUST start by calling get_files_info to find out what files and directories exist.
    - DO NOT guess file paths. Only access or run files that you have seen in the output of get_files_info.
    - All paths you provide must be relative to the working directory. Do not specify the working directory in your tool calls as it is automatically injected.
    """

    ######## Chat with Ollama (local) #########
    client = ollama.Client(host='http://127.0.0.1:11434')
    model = "llama3.1:8b"
    
    messages = [
        {"role": "system", "content": system_prompt},
        # Few-shot example to teach llama3.1:8b native tool calling and recovery
        {"role": "user", "content": "find the implementation of calculator"},
        {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "get_files_info", "arguments": {"directory": "."}}}]},
        {"role": "tool", "tool_name": "get_files_info", "content": "main.py, size: 1204 bytes\npkg/ , size: 4096 bytes\n"},
        {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "get_file_content", "arguments": {"file_path": "main.py"}}}]},
        {"role": "tool", "tool_name": "get_file_content", "content": "import pkg.calculator"},
        {"role": "assistant", "content": "The calculator implementation is imported in main.py from the pkg directory."},
        # Actual user query
        {"role": "user", "content": user_prompt}
    ]

    available_functions = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'write_file': write_file,
        'run_python_file': run_python_file,
    }

    max_iterations = 20
    for i in range(max_iterations):
        response = client.chat(
            model=model,
            messages=messages,
            tools=[get_files_info, get_file_content, write_file, run_python_file]
        )

        # Append assistant's response to history
        messages.append(response.message)

        if response.message.tool_calls:
            for tool in response.message.tool_calls:
                func_name = tool.function.name
                func_args = tool.function.arguments
                
                if verbose:
                    print(f"Calling function: {func_name}")
                    print(f"Arguments: {func_args}")
                
                func_to_call = available_functions.get(func_name)
                if func_to_call:
                    try:
                        if func_args is None:
                            func_args = {}
                        result = func_to_call(**func_args)
                    except Exception as e:
                        result = f"Error executing tool {func_name}: {e}"
                else:
                    result = f"Error: function {func_name} is not available"

                messages.append({
                    'role': 'tool',
                    'tool_name': func_name,
                    'content': str(result)
                })
        else:
            # final agent text response
            print(response.message.content)
            
            # Token tracking
            if verbose:
                prompt_eval = getattr(response, "prompt_eval_count", 0) or 0
                eval_count = getattr(response, "eval_count", 0) or 0
                print(f"user prompt: {user_prompt}")
                print(f"prompt tokens used: {prompt_eval}")
                print(f"response tokens used: {eval_count}")
                print(f"total tokens used: {prompt_eval + eval_count}")
            break

if __name__ == "__main__":
    main()