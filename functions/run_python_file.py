import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory:str, file_path:str, args:list[str] = []):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(absolute_working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: file "{file_path}" is not in the working directory'
    
    if not os.path.exists(absolute_file_path):
        return f'Error: file "{file_path}" does not exist'
    
    if os.path.isdir(absolute_file_path):
        return f'Error: file "{file_path}" is a directory'

    if not file_path.endswith(".py"):
        return f'Error: file "{file_path}" is not a Python file'

    try:
        final_args = ["python", absolute_file_path] + args
        output = subprocess.run(
            final_args, 
            timeout=30,
            cwd=absolute_working_directory,
            capture_output=True,
            text=True
        )
        return f"""
            STDOUT: {output.stdout}
            STDERR: {output.stderr}
            Return Code: {output.returncode}
            """
    
    except Exception as e:
        return f"Error: {absolute_file_path}: could not be executed: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a python file and returns its output. accepts addition cli args as an optional array ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, 
                description="path to the python file to run, relative to working directory"
                ),
            "args": types.Schema(
                type=types.Type.ARRAY, 
                description="array of strings representing the cli arguments to pass to the python script",
                items=types.Schema(
                    type=types.Type.STRING,
                    )
                )
        }
    )
)