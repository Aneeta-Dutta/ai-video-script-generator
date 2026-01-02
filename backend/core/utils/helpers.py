"""
Shared utilities for AI Video Production System.

Provides common helpers for file I/O, retries, timing, and more.
"""

import time
import functools
from typing import Callable, Any, Optional, TypeVar, cast
from pathlib import Path
import json


T = TypeVar('T')


def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator to retry a function on failure with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each attempt
        exceptions: Tuple of exceptions to catch
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        raise
            
            # This should never be reached, but helps with type checking
            raise cast(Exception, last_exception)
        
        return wrapper
    return decorator


def timer(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Attach duration to result if possible
        if hasattr(result, '__dict__'):
            result.__dict__['_execution_time_ms'] = duration
        
        return result
    return wrapper


def load_json_file(file_path: Path) -> dict:
    """
    Load JSON file safely.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        Parsed JSON content
    
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data: dict, file_path: Path, indent: int = 2):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save file
        indent: JSON indentation level
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_text_file(file_path: Path) -> str:
    """
    Load text file safely.
    
    Args:
        file_path: Path to text file
    
    Returns:
        File content as string
    
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def save_text_file(content: str, file_path: Path):
    """
    Save text content to file.
    
    Args:
        content: Text content to save
        file_path: Path to save file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """
    Sanitize filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        replacement: Character to replace invalid chars with
    
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, replacement)
    return filename


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
