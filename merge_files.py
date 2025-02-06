import os
from pathlib import Path
from typing import Union, List

def validate_paths(paths: List[Path]) -> None:
    """
    Validate that all paths exist and are accessible.
    
    Args:
        paths: List of Paths to validate
    
    Raises:
        FileNotFoundError: If any path doesn't exist
        PermissionError: If any path isn't readable
        ValueError: If a path is a directory when expecting a file, or vice versa
    """
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        if not os.access(path, os.R_OK):  # Correct way to check readability
            raise PermissionError(f"Path is not readable: {path}")

def merge_files_to_string(paths: Union[Path, List[Path]], lenient: bool = False) -> str:
    """
    Merge contents of files into one large string.
    
    Args:
        paths: Path or list of Paths (can be mix of directories and files)
        lenient: If True, skip invalid files instead of raising errors
    
    Returns:
        Concatenated string of all file contents
    """
    merged_text = []
    
    # Convert single path to list for consistent processing
    if isinstance(paths, Path):
        paths = [paths]
    
    # Collect all files from directories and individual files
    file_paths = []
    for path in paths:
        if path.is_dir():
            file_paths.extend(path.glob("**/*.py"))  # Default to .py files for directories
        else:
            file_paths.append(path)
    
    # Validate paths (unless in lenient mode)
    if not lenient:
        try:
            validate_paths(file_paths)
        except (FileNotFoundError, PermissionError, ValueError) as e:
            raise RuntimeError(f"Invalid paths detected (strict mode): {str(e)}")
    
    for file_path in file_paths:
        print(file_path)
        try:
            if lenient:
                validate_paths([file_path])
            with file_path.open('r', encoding='utf-8') as f:
                merged_text.append(f"\n\n--- {file_path.name} ---\n\n")
                merged_text.append(f.read())
        except (FileNotFoundError, PermissionError, ValueError, UnicodeDecodeError) as e:
            if lenient:
                print(f"Skipping {file_path} due to {type(e).__name__}: {str(e)}")
            else:
                raise
    
    return ''.join(merged_text)
