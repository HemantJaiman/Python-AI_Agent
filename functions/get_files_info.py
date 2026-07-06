import os

from google.genai import types

def get_files_info(working_directory: str, directory: str = "." ) -> str:
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_directory = os.path.abspath(os.path.join(absolute_working_directory, directory))

    if not absolute_directory.startswith(absolute_working_directory):
        return f'Error: directory "{directory}" is not in the working directory'
    
    content = os.listdir(absolute_directory)
    
    files = ""
    for item in content:
        item_path = os.path.join(absolute_directory, item)
        item_size = os.path.getsize(item_path)
        if os.path.isdir(item_path):
            files += f"{item}/ , size: {item_size} bytes\n"
        else:
            files += f"{item}, size: {item_size} bytes \n" 
    return files

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="lists files and directories in the specified directory along with file sizes",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING, 
                description="this directory to list files from, relative to working directory.if not provided, lists files in the working directory itself"
                )
        }
    )
)