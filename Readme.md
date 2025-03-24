Project README

## Setup

### Prerequisites

- Python 3.7 or higher
- Flask
- OpenAI API key
- Required Python packages (listed below)

### Installation

1. **Clone the repository**:
   git clone <repository_url>
   cd <project_directory>

2. **Create a Virtual Environment** (optional but recommended):
   - For **Windows**:
     python -m venv venv
     venv\Scripts\activate
   - For **macOS/Linux**:
     python3 -m venv venv
     source venv/bin/activate

3. **Install the required dependencies**:
   pip install -r requirements.txt

4. **Set your OpenAI API key in an environment variable**:
   - For **Windows**:
     set OPENAI_API_KEY="your-api-key"
   - For **macOS/Linux**:
     export OPENAI_API_KEY="your-api-key"

5. **Run the Flask app**:
   python app.py

   The application will be running on `http://127.0.0.1:5000/` by default.

## API Endpoints

### `/chat` (POST)

**Description**: This endpoint handles user requests to either generate a new project or modify existing files.

**Request Body**:
{
  "message": "User's request (either 'create new project' or 'modify existing project')"
}

**Response**:
- On successful project generation or modification, a success message is returned:
  {
    "response": "✅ New project 'project_name' created!"  // or modified successfully
  }

## File Structure

The generated and modified files are stored in the `generated_projects` directory. Each project is stored in its own folder with the name of the project. The folder will contain the following files by default:

- `index.html`: The HTML structure of the project.
- `style.css`: The styles for the project.
- `script.js`: The JavaScript code for the project.

## Example Requests

### 1. Generating a new project:

**Request**:
{
  "message": "Create a new project called 'MyWebsite'."
}

**Response**:
{
  "response": "✅ New project 'MyWebsite' created!"
}

### 2. Modifying an existing project:

**Request**:
{
  "message": "Modify the index.html of 'MyWebsite' to include a footer."
}

**Response**:
{
  "response": "✅ Modified 'generated_projects/MyWebsite/index.html' successfully!"
}

## Backend Workflow

1. **Chat Request Handling**: When a user sends a request, the Flask app processes the message and determines whether the request is to generate or modify a project.
2. **Generate Project**: If the request is to generate a new project, the system creates the necessary files and stores them in a folder named after the project in the `generated_projects` directory.
3. **Modify Project**: If the request is to modify an existing project, the system fetches the current content of the files to be modified, appends the user's modification prompt, and sends this data back to OpenAI to generate the updated content. The files are then updated with the new content.

## File Modification Details

- Modifications are handled by collecting the content of the specified files, appending the modification request to the content, and sending it back to OpenAI to generate the new file content.
- The backend ensures that the modified files are updated in the project folder and the changes are persisted.

## Helper Functions

- `integrate_generated_files`: Integrates the generated files into the appropriate project folder.
- `create_project_files`: Creates files in a new project.
- `modify_project_files`: Modifies the existing files based on the specified content.
- `update_file`: Updates a specific file with new content.
- `append_file_content_and_prompt`: Fetches the content of files, appends it with the modification prompt, and prepares the request for OpenAI.

