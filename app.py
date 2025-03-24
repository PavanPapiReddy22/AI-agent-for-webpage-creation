from flask import Flask, request, jsonify, render_template
import os
import json
from openai import OpenAI
from models import FileCreationRequest, FileModificationRequest, FileResponse
from tools import integrate_generated_files, update_file, append_file_content_and_prompt

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are an expert frontend developer assistant.

[A] GENERATE:
If the user requests a new project, generate a **plain HTML, CSS, and JavaScript** project. All generated files should be placed in a folder named after the project within the `generated_projects` directory.

Respond strictly in JSON:

{
  "type": "generate",
  "project_name": "explicit-project-name",
  "file_structure": {
    "index.html": "...",
    "style.css": "...",
    "script.js": "..."
  }
}

[B] MODIFY:
If the user requests a modification, **you will only receive the file paths to modify** (with `"type": "modify"`) and you should **not generate any content directly**.

Instead, first gather the content of the specified files (which will be done in the backend), **append** them together with the user's prompt, and **send the combined data back to you**. Upon receiving this combined data, you will generate the final modification for each file.

Your output should **only include the full file paths to the files that need modification**, without any code. The format should look like this:

{
  "type": "modify",
  "modifications": {
    "generated_projects/{project_name}/path-to-file1": "file1",
    "generated_projects/{project_name}/path-to-file2": "file2"
    . . .
  }
}
The output should be strictly in Json formet
"""

projects = {}  # Store project states


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response_data = process_request(user_message)
    print(response_data)
    

    if response_data["type"] == "generate":
        return jsonify({"response": handle_generation(response_data)})
    elif response_data["type"] == "modify":
        return jsonify({"response": handle_modification(response_data, user_message)})

    return jsonify({"response": "⚠️ Unknown request type."})


def process_request(prompt: str) -> dict:
    """LLM processes the user request and determines the action (generate or modify)."""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        # response_format="json",  # Ensure we return in JSON format
    )
    return json.loads(completion.choices[0].message.content)


def process_request_2(prompt: str) -> dict:
    system_prompt = """
You are an AI that modifies files based on user instructions. Your task is to update the content of files, ensuring that the old content is replaced with the new content. 

For each file modification request, you must return a JSON object with the following structure:
- "file_path": The path of the file to be modified.
- "new_content": The updated content of the file after the change.

you will get the old code and the modification prompt 
you should modify that code and return it in the below format

Example format:
{
    "modified_files": [
        {
            "file_path": "path/to/file1.txt",
            "new_content": "new content for file 1"
        },
        {
            "file_path": "path/to/file2.txt",
            "new_content": "new content for file 2"
        }
    ]
}

Ensure that:
just the above formet nothing else 
dont output these kind of things
```json like these
...
    """

    # Send request to OpenAI API
    completion_2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        # response_format="json",
    )

    
   

    # Attempt to load the response as JSON
    return json.loads(completion_2.choices[0].message.content)


def handle_generation(response_data: dict) -> str:
    """Handles project generation based on LLM response."""
    project_name = response_data["project_name"]
    file_structure = response_data["file_structure"]

    projects[project_name] = file_structure
    integrate_generated_files(project_name, file_structure)

    return f"✅ New project '{project_name}' created!"


def handle_modification(response_data: dict, user_message: str) -> str:
    """Handles multiple file modifications based on LLM response."""
    # In this version, we only receive file paths for modification
    modifications = response_data["modifications"]
    

    # Collect file paths from the modifications
    file_paths = list(modifications.keys())

    # Use the new tool to fetch file content and append it to the user prompt
    combined_content = append_file_content_and_prompt(file_paths, modifications)
    
    combined_content = combined_content + "\n" + user_message

    # Now send the combined content and user prompt to the LLM to generate the final modification
    final_response_data = process_request_2(combined_content)

    print(final_response_data)

    # Continue the usual process of updating files with the final content
    # Apply the final modifications
    modified = []
    for file_data in final_response_data["modified_files"]:  # Iterate over a list
        file_path = file_data["file_path"]
        new_content = file_data["new_content"]

        try:
            update_file(file_path, new_content)
            modified.append(file_path)
        except FileNotFoundError:
            return f"⚠️ File '{file_path}' not found."

    return f"✅ Modified {', '.join(modified)} successfully!"


if __name__ == "__main__":
    app.run(debug=True)
