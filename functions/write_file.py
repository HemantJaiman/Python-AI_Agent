import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(absolute_working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: file "{file_path}" is not in the working directory'
    
    if not os.path.isfile(absolute_file_path):
        try:
            os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: {absolute_file_path}: Directory could not be created: {e}"

    try:
        with open(absolute_file_path, "w") as file:
            file.write(content)
        return f"Success: {absolute_file_path}: {len(content)} characters written successfully."
    except Exception as e:
        return f"Error: {absolute_file_path}: could not be written: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes the given content to a file at the specified file path. Creates the file and parent directories if they do not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, 
                description="the path to the file to write, relative to the working directory"
                ),
            "content": types.Schema(
                type=types.Type.STRING, 
                description="the content to write to the file"
                ),
        }
    )
)