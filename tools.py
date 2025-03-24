import os
from typing import Dict, List
import json

BASE_DIR = "generated_projects"


def integrate_generated_files(
    project_name: str, file_structure: Dict[str, str]
) -> List[str]:
    project_path = os.path.join(BASE_DIR, project_name)
    file_paths = []

    for relative_path, content in file_structure.items():
        file_path = os.path.join(project_path, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        file_paths.append(file_path)
        print(f"✅ Integrated: {file_path}")

    return file_paths


def create_project_files(
    project_name: str, file_structure: Dict[str, str]
) -> Dict[str, List[str]]:
    project_path = os.path.join(BASE_DIR, project_name)
    os.makedirs(project_path, exist_ok=True)

    created_file_paths = []
    for file_name, content in file_structure.items():
        file_path = os.path.join(project_path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        created_file_paths.append(file_path)
        print(f"✅ Created file: {file_path}")

    return {"project_path": project_path, "file_paths": created_file_paths}


def modify_project_files(file_modifications: List[Dict[str, str]]) -> List[str]:
    modified_files = []

    for mod in file_modifications:
        file_path = mod["file_path"]
        new_content = mod["modified_content"]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"⚠️ File {file_path} not found.")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)

        modified_files.append(file_path)
        print(f"✅ Modified file: {file_path}")

    return modified_files


def update_file(file_path: str, new_content: str):
    """Updates a specific file with the given content."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"⚠️ File {file_path} not found.")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_content)

    print(f"✅ File updated: {file_path}")


def append_file_content_and_prompt(file_paths: list, modifications: dict) -> str:
    """Fetches the content of files, appends them to the user prompt, and prepares the request for LLM."""
    # Retrieve the content of the files
    file_contents = ""
    for file_path in file_paths:
        try:
            with open(file_path, "r") as file:
                file_contents += file.read() + "\n"
        except FileNotFoundError:
            return f"⚠️ File '{file_path}' not found."

    # Combine the contents of the files with the user prompt
    user_prompt = "Please modify the following files based on the provided content:\n"
    user_prompt += f"Files to modify:\n{json.dumps(modifications, indent=2)}\n\n"
    user_prompt += f"Current file contents:\n{file_contents}\n"

    return user_prompt
