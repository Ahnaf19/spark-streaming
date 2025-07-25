import os
from pathlib import Path
from loguru import logger


def get_project_root() -> Path:
    """Get the project root directory by looking for key project files."""
    current_path = Path(__file__).resolve()
    
    # Traverse up the directory tree to find the project root
    for parent in current_path.parents:
        # Check for project indicators (requirements.txt, README.md, etc.)
        if (parent / "requirements.txt").exists() and (parent / "README.md").exists():
            return parent
    
    # Fallback: assume project root is 2 levels up from this file
    # (streaming/utils/utils.py -> project root)
    return current_path.parent.parent.parent


def setup_data_input_path(input_path: str = "data/input") -> str:
    """
    Set up the data input path for CSV files.
    
    Args:
        input_path: Relative path from project root (default: "data/input")
    
    Returns:
        Absolute path to the input directory
    """
    project_root = get_project_root()
    data_input_path = project_root / input_path
    
    # Convert to absolute path string for compatibility
    data_input_path_str = str(data_input_path.resolve())
    
    logger.info(f"Project root: {project_root}")
    logger.info(f"Setting up stream read from dir: {data_input_path_str}")

    # Check if input directory doesn't exist
    if not data_input_path.exists():
        logger.warning(f"Input directory: {data_input_path_str} does not exist. Creating...")
        data_input_path.mkdir(parents=True, exist_ok=True)
        logger.success(f"Created missing input directory: {data_input_path_str}")
    else:
        logger.info(f"Input directory already exists: {data_input_path_str}")
        
    return data_input_path_str