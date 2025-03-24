from pydantic import BaseModel, Field
from typing import List, Dict


class FileCreationRequest(BaseModel):
    """Request model for generating frontend files."""

    project_name: str = Field(description="Name of the frontend project")
    file_structure: Dict[str, str] = Field(
        description="Dictionary defining file names and contents"
    )


class FileModificationRequest(BaseModel):
    """Request model for modifying multiple files."""

    modifications: Dict[str, str] = Field(
        description="A dictionary of file paths and their modified content"
    )


class FileResponse(BaseModel):
    """Response model for file operations."""

    message: str = Field(description="Success message")
    file_paths: List[str] = Field(description="List of created or modified file paths")
