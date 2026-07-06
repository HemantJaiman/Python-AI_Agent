from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from google.genai import types


working_directory = "calculator"

def call_functions(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}")
        print(f"Arguments: {function_call_part.args}")
    result = None
    match function_call_part.name:
        case "get_files_info":
            result =  get_files_info(working_directory, function_call_part.args.get("directory", "."))
        case "get_file_content":
            result =  get_file_content(working_directory, function_call_part.args["file_path"])
        case "write_file":
            result =  write_file(working_directory, function_call_part.args["file_path"], function_call_part.args["content"])
        case "run_python_file":
            result =  run_python_file(working_directory, function_call_part.args["file_path"], function_call_part.args["args"])
    
    return types.Content(
        role="tool", 
        parts=[types.Part(function_response=types.FunctionResponse(name=function_call_part.name,
         response={"response": result}))])    