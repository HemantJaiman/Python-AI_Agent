import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory: str, file_path: str) -> str:
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(absolute_working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: file "{file_path}" is not in the working directory'
    
    if not os.path.exists(absolute_file_path):
        return f'Error: file "{file_path}" does not exist'
    
    if os.path.isdir(absolute_file_path):
        return f'Error: file "{file_path}" is a directory'

    file_content_str = ""

    try:
        with open(absolute_file_path, "r") as file:
            file_content_str = file.read(MAX_CHARS)
            if len(file_content_str) >= MAX_CHARS:
                file_content_str += "\n[TRUNCATED] - More content available"
        return file_content_str
    except Exception as e:
        return f'Error: file "{file_path}" could not be read - {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="get the content of the given file as a string, contrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, 
                description="path to the file, relative to working directory"
                )
        }
    )
)