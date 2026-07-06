
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main() -> None:
    work_dir = "calculator"
    #content = get_file_content(work_dir, "lorem.txt")
    #print(content)
    #print(get_file_content(work_dir, "pkg/calculator.py"))
    #print(get_file_content(work_dir, "main.py"))
    #print(write_file(work_dir, "lorem.txt", "Hello World. This is a test."))
    #print(write_file(work_dir, "pkg/new_created_file", "Hello from Testing from root to cerate new file"))
    print(run_python_file(work_dir, "main.py", ["5 + 5"]))

if __name__ == "__main__":
    main()