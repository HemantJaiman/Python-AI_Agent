import os


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
