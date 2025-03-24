# Project README

## Setup

### Prerequisites

- Python 3.7 or higher
- Flask
- OpenAI API key
- Required Python packages (listed below)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Create a Virtual Environment** (optional but recommended):
   - For **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - For **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key in an environment variable**:
   - For **Windows**:
     ```bash
     set OPENAI_API_KEY="your-api-key"
     ```
   - For **macOS/Linux**:
     ```bash
     export OPENAI_API_KEY="your-api-key"
     ```

5. **Run the Flask app**:
   ```bash
   python app.py
   ```

   The application will be running on `http://127.0.0.1:5000/` by default.

---

## API Endpoints

### `/chat` (POST)

**Description**: This endpoint handles user requests to either generate a new project or modify existing files.

**Request Body**:
```json
{
  "message": "User's request (either 'create new project' or 'modify existing project')"
}
```

**Response**:
- On successful project generation or modification, a success message is returned:
```json
{
  "response": "✅ New project 'project_name' created!  or modified successfully"
}
```

---

## File Structure

The generated and modified files are stored in the `generated_projects` directory. Each project is stored in its own folder with the name of the project. The folder will contain the following files by default:
- `index.html`: The HTML structure of the project.
- `style.css`: The styles for the project.
- `script.js`: The JavaScript code for the project.

---

## Example Requests

### 1. Generating a new project:

**Request**:
```json
{
  "message": "Generate a new project called 'MyWebsite'."
}
```

**Response**:
```json
{
  "response": "✅ New project 'MyWebsite' created!"
}
```

### 2. Modifying an existing project:

**Request**:
```json
{
  "message": "Modify the index.html of 'MyWebsite' to include a footer."
}
```

**Response**:
```json
{
  "response": "✅ Modified 'generated_projects/MyWebsite/index.html' successfully!"
}
```

---

## Project Flow

### Trigger Mechanism

- **For Creating a Project**: The LLM identifies the user’s intent to create a new project by recognizing the keyword `generate` (or similar language) in the user's message.
  - Example: `Generate a new project called 'MyWebsite'`.

- **For Modifying a Project**: The LLM identifies the user's intent to modify an existing project by recognizing the keyword `modify` (or similar language) in the user's message.
  - Example: `Modify the index.html of 'MyWebsite' to include a footer.`

### Create Project Flow

1. **User sends a request**: The user requests to create a new project. The LLM interprets the user's message and identifies the need to generate a new project based on the `generate` trigger.
   
2. **Flask app processes the request**: Upon detecting the `generate` keyword, the Flask app processes the message to trigger the project creation flow.

3. **Files are generated**: The system creates the necessary files for the project (e.g., `index.html`, `style.css`, `script.js`) and stores them in a folder named after the project in the `generated_projects` directory.

4. **Success response**: After the project files are created, the Flask app responds with a success message:  
   `"✅ New project 'MyWebsite' created!"`

### Modify Project Flow

1. **User sends a modification request**: The user requests to modify an existing project. The LLM interprets the message and identifies the need to modify specific project files based on the `modify` keyword.
   
2. **Flask app processes the request**: Upon detecting the `modify` keyword, the Flask app processes the request and triggers the project modification process.

3. **Fetch current file content**: The system fetches the current content of the file(s) to be modified (e.g., `index.html`, `style.css`).

4. **Modification is applied**: The modification request is appended to the file content, user prompt is also appended to the file content, and the updated content is sent to OpenAI for processing.

5. **File is updated**: The modified file is updated with the new content and stored in the appropriate project folder.

6. **Success response**: The Flask app responds with a success message indicating the file has been modified:  
   `"✅ Modified 'generated_projects/MyWebsite/index.html' successfully!"`

---

## File Modification Details

- Modifications are handled by fetching the content of the specified files, appending the modification request to the content, and sending it back to OpenAI to generate the new file content.
- The backend ensures that the modified files are updated in the project folder, and the changes are persisted.

---

## Tools

- `integrate_generated_files`: Integrates the generated files into the appropriate project folder.
- `create_project_files`: Creates the necessary files for a new project.
- `modify_project_files`: Modifies the existing files based on the specified content.
- `update_file`: Updates a specific file with new content.
- `append_file_content_and_prompt`: Fetches the content of the specified files, appends it with the modification prompt, and prepares the request for OpenAI.

---
