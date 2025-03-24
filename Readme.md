\documentclass{article}
\usepackage{listings}
\usepackage{graphicx}

\title{Project README}
\author{}
\date{}

\begin{document}

\maketitle

\section*{Setup}

\subsection*{Prerequisites}

\begin{itemize}
    \item Python 3.7 or higher
    \item Flask
    \item OpenAI API key
    \item Required Python packages (listed below)
\end{itemize}

\subsection*{Installation}

\begin{enumerate}
    \item \textbf{Clone the repository}:
    \begin{lstlisting}[language=bash]
    git clone <repository_url>
    cd <project_directory>
    \end{lstlisting}

    \item \textbf{Create a Virtual Environment} (optional but recommended):
    \begin{itemize}
        \item For \textbf{Windows}:
        \begin{lstlisting}[language=bash]
        python -m venv venv
        venv\Scripts\activate
        \end{lstlisting}
        \item For \textbf{macOS/Linux}:
        \begin{lstlisting}[language=bash]
        python3 -m venv venv
        source venv/bin/activate
        \end{lstlisting}
    \end{itemize}

    \item \textbf{Install the required dependencies}:
    \begin{lstlisting}[language=bash]
    pip install -r requirements.txt
    \end{lstlisting}

    \item \textbf{Set your OpenAI API key in an environment variable}:
    \begin{itemize}
        \item For \textbf{Windows}:
        \begin{lstlisting}[language=bash]
        set OPENAI_API_KEY="your-api-key"
        \end{lstlisting}
        \item For \textbf{macOS/Linux}:
        \begin{lstlisting}[language=bash]
        export OPENAI_API_KEY="your-api-key"
        \end{lstlisting}
    \end{itemize}

    \item \textbf{Run the Flask app}:
    \begin{lstlisting}[language=bash]
    python app.py
    \end{lstlisting}

    The application will be running on \texttt{http://127.0.0.1:5000/} by default.
\end{enumerate}

\section*{API Endpoints}

\subsection*{\texttt{/chat} (POST)}

\textbf{Description}: This endpoint handles user requests to either generate a new project or modify existing files.

\textbf{Request Body}:
\begin{lstlisting}[language=json]
{
  "message": "User's request (either 'create new project' or 'modify existing project')"
}
\end{lstlisting}

\textbf{Response}:
\begin{itemize}
    \item On successful project generation or modification, a success message is returned:
\begin{lstlisting}[language=json]
{
  "response": "✅ New project 'project_name' created!"  // or modified successfully
}
\end{lstlisting}
\end{itemize}

\section*{File Structure}

The generated and modified files are stored in the \texttt{generated\_projects} directory. Each project is stored in its own folder with the name of the project. The folder will contain the following files by default:
\begin{itemize}
    \item \texttt{index.html}: The HTML structure of the project.
    \item \texttt{style.css}: The styles for the project.
    \item \texttt{script.js}: The JavaScript code for the project.
\end{itemize}

\section*{Example Requests}

\subsection*{1. Generating a new project:}

\textbf{Request}:
\begin{lstlisting}[language=json]
{
  "message": "Generate a new project called 'MyWebsite'."
}
\end{lstlisting}

\textbf{Response}:
\begin{lstlisting}[language=json]
{
  "response": "✅ New project 'MyWebsite' created!"
}
\end{lstlisting}

\subsection*{2. Modifying an existing project:}

\textbf{Request}:
\begin{lstlisting}[language=json]
{
  "message": "Modify the index.html of 'MyWebsite' to include a footer."
}
\end{lstlisting}

\textbf{Response}:
\begin{lstlisting}[language=json]
{
  "response": "✅ Modified 'generated_projects/MyWebsite/index.html' successfully!"
}
\end{lstlisting}

\section*{Project Flow}

\subsection*{Trigger Mechanism}

\begin{itemize}
    \item \textbf{For Creating a Project}: The LLM identifies the user’s intent to create a new project by recognizing the keyword \texttt{generate} (or similar language) in the user's message.
    \begin{itemize}
        \item Example: \texttt{Generate a new project called 'MyWebsite'}.
    \end{itemize}
    \item \textbf{For Modifying a Project}: The LLM identifies the user's intent to modify an existing project by recognizing the keyword \texttt{modify} (or similar language) in the user's message.
    \begin{itemize}
        \item Example: \texttt{Modify the index.html of 'MyWebsite' to include a footer.}
    \end{itemize}
\end{itemize}

\subsection*{Create Project Flow}

\begin{enumerate}
    \item \textbf{User sends a request}: The user requests to create a new project. The LLM interprets the user's message and identifies the need to generate a new project based on the \texttt{generate} trigger.
    \item \textbf{Flask app processes the request}: Upon detecting the \texttt{generate} keyword, the Flask app processes the message to trigger the project creation flow.
    \item \textbf{Files are generated}: The system creates the necessary files for the project (e.g., \texttt{index.html}, \texttt{style.css}, \texttt{script.js}) and stores them in a folder named after the project in the \texttt{generated\_projects} directory.
    \item \textbf{Success response}: After the project files are created, the Flask app responds with a success message:
    \begin{lstlisting}[language=json]
    "✅ New project 'MyWebsite' created!"
    \end{lstlisting}
\end{enumerate}

\subsection*{Modify Project Flow}

\begin{enumerate}
    \item \textbf{User sends a modification request}: The user requests to modify an existing project. The LLM interprets the message and identifies the need to modify specific project files based on the \texttt{modify} keyword.
    \item \textbf{Flask app processes the request}: Upon detecting the \texttt{modify} keyword, the Flask app processes the request and triggers the project modification process.
    \item \textbf{Fetch current file content}: The system fetches the current content of the file(s) to be modified (e.g., \texttt{index.html}, \texttt{style.css}).
    \item \textbf{Modification is applied}: The modification request is appended to the file content, and the updated content is sent to OpenAI for processing.
    \item \textbf{File is updated}: The modified file is updated with the new content and stored in the appropriate project folder.
    \item \textbf{Success response}: The Flask app responds with a success message indicating the file has been modified:
    \begin{lstlisting}[language=json]
    "✅ Modified 'generated_projects/MyWebsite/index.html' successfully!"
    \end{lstlisting}
\end{enumerate}

\section*{File Modification Details}

\begin{itemize}
    \item Modifications are handled by fetching the content of the specified files, appending the modification request to the content, and sending it back to OpenAI to generate the new file content.
    \item The backend ensures that the modified files are updated in the project folder, and the changes are persisted.
\end{itemize}

\section*{Helper Functions}

\begin{itemize}
    \item \texttt{integrate\_generated\_files}: Integrates the generated files into the appropriate project folder.
    \item \texttt{create\_project\_files}: Creates the necessary files for a new project.
    \item \texttt{modify\_project\_files}: Modifies the existing files based on the specified content.
    \item \texttt{update\_file}: Updates a specific file with new content.
    \item \texttt{append\_file\_content\_and\_prompt}: Fetches the content of the specified files, appends it with the modification prompt, and prepares the request for OpenAI.
\end{itemize}

\section*{License}

This project is open-source and available under the \href{LICENSE}{MIT License}.

\end{document}
