import json
from pathlib import Path
from datetime import datetime
import re
from typing import List


class Store:
    """
    A simple file-based store for workshop folders. Each student has a folder named 'student-XXX'
    where XXX is a zero-padded number (e.g. 'student-001', 'student-002', etc.). The store can
    list existing student folders, create new ones, and determine which one to use based on
    recent activity.
    """

    def __init__(self, base_path: str = "data/students", name_prefix: str = "student"):
        self.base_path = Path(base_path)
        self.name_prefix = name_prefix
        self.pattern = re.compile(rf"{re.escape(name_prefix)}-(\d{{3}})$")

        if not self.base_path.exists():
            raise FileNotFoundError(f"Folder not found: {self.base_path}")

        if not self.base_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {self.base_path}")
        
    def _folder(self, folder: Path) -> dict:
        """
        Helper method to convert a folder Path to a dictionary with name and last_modified.
        
        Args:
            folder (Path): The folder to convert.
            
        Returns:
             A dictionary with 'name' and 'last_modified' (as a datetime object) of the folder.
        """
        match = self.pattern.match(folder.name)
        return {
            "name": folder.name,
            "last_modified": datetime.fromtimestamp(folder.stat().st_mtime),
            "index": int(match.group(1)) if match else 0,
        }

    def list(self) -> list[dict]:
        """
        List all subfolders inside the base path with their last modification time.

        Returns:
            A list of dictionaries with:
            - name: folder name
            - last_modified: readable timestamp (YYYY-MM-DD HH:MM:SS)
        """
        return [ self._folder(folder) for folder in self.base_path.iterdir() if folder.is_dir() ]
    
    def last(self) -> dict | None:
        """
        Get the most recently modified folder.

        Returns:
            A dictionary with 'name' and 'last_modified' of the most recent folder, or None if no folders exist.
        """
        folders = self.list()
        if not folders:
            return None
        return max(folders, key=lambda f: f["last_modified"])
    
    def recent(self, hours: int = 24) -> dict | None:
        """
        Check if the most recently modified folder was modified within the last given hours.

        Args:
            hours (int): The number of hours to consider for recent activity (default is 24).

        Returns:
            True if the most recent folder was modified within the last given hours, False otherwise.
        """
        last_folder = self.last()
        now = datetime.now()
        return last_folder if last_folder is not None and (now - last_folder["last_modified"]).total_seconds() < hours * 3600 else None
    
    def max_nummber(self) -> int:
        """
        Get the maximum number used in existing folder names.

        Returns:
            The maximum number found in existing folder names, or 0 if no folders exist.
        """
        return max([ f["index"] for f in self.list() ], default=0)
    
    def create(self) -> str:
        """
        Create a new folder with name '<prefix>-XXX'
        where XXX is the next available number (zero-padded to 3 digits).

        Returns:
            The name of the created folder.
        """
        new_folder_name = f"{self.name_prefix}-{self.max_nummber() + 1:03d}"
        new_folder_path = self.base_path / new_folder_name
        new_folder_path.mkdir()
        return new_folder_name
    
    def create_or_recent(self, hours: int = 24) -> str:
        """
        Return the most recently modified folder if it was modified within the last given hours.
        Otherwise, create and return a new folder.

        Args:
            hours (int): The number of hours to consider for recent activity (default is 24).
        
        Returns:
            The folder name (e.g. 'student-003').
        """
        recent_folder = self.recent(hours=hours)
        if recent_folder:
            return recent_folder["name"]
        return self.create()
    

    def save_chunks(self, user: str, chunks: List[str]) -> None:
        """
        Save a list of text chunks to a file named 'chunks.json' inside the user's folder.

        Args:
            user (str): The name of the user's folder (e.g. 'student-003').
            chunks (list[str]): A list of text chunks to save.
        """
        user_folder = self.base_path / user
        user_folder.mkdir(exist_ok=True)  # Ensure the user folder exists
        chunks_file = user_folder / "chunks.json"
        with chunks_file.open("w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2)

    def save_extracted_statements(self, user: str, chunk_index: int, statements: List[dict]) -> None:
        """
        Save extracted statements for a specific chunk within a user's folder.

        Args:
            user (str): The name of the user's folder (e.g. 'student-003').
            chunk_index (int): The index of the chunk within the user's folder.
            statements (list[dict]): A list of extracted statements to save.
        """
        user_folder = self.base_path / user
        user_folder.mkdir(exist_ok=True)  # Ensure the user folder exists
        statements_file = user_folder / f"statements-{chunk_index}.json"
        with statements_file.open("w", encoding="utf-8") as f:
            json.dump(statements, f, indent=2)

    def load_chunks(self, user: str) -> List[str]:
        """
        Load a list of text chunks from a file named 'chunks.json' inside the user's folder.

        Args:
            user (str): The name of the user's folder (e.g. 'student-003').

        Returns:
            A list of text chunks loaded from the file, or an empty list if the file does not exist.
        """
        chunks_file = self.base_path / user / "chunks.json"
        if not chunks_file.exists():
            return []
        with chunks_file.open("r", encoding="utf-8") as f:
            return json.load(f)