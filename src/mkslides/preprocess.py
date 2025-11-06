import importlib
import importlib.util
import logging
from pathlib import Path
from typing import Callable, Optional

logger = logging.getLogger(__name__)

PREPROCESS_FUNCTION_NAME = "preprocess"
PREPROCESS_FILE_FUNCTION_NAME = "preprocess_file"


def load_preprocessing_function(script: str) -> Optional[Callable[[str], str]]:
    spec = importlib.util.spec_from_file_location("preprocess_module", script)
    if spec is None:
        message = f"Could not create module spec from '{script}'"
        raise ImportError(message)

    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        message = f"Module spec for '{script}' has no loader"
        raise ImportError(message)

    spec.loader.exec_module(module)
    preprocess_func = getattr(module, PREPROCESS_FUNCTION_NAME, None)

    if not preprocess_func:
        message = f"Could not find '{PREPROCESS_FUNCTION_NAME}' function in '{script}'"
        raise ValueError(message)

    logger.debug(f"Loaded preprocessing function from '{script}'")

    return preprocess_func


def load_file_preprocessing_function(script: str) -> Optional[Callable[[Path], Optional[Path]]]:
    """Load a file preprocessing function that takes a file path and returns an optional new path."""
    spec = importlib.util.spec_from_file_location("preprocess_file_module", script)
    if spec is None:
        message = f"Could not create module spec from '{script}'"
        raise ImportError(message)

    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        message = f"Module spec for '{script}' has no loader"
        raise ImportError(message)

    spec.loader.exec_module(module)
    preprocess_func = getattr(module, PREPROCESS_FILE_FUNCTION_NAME, None)

    if not preprocess_func:
        message = f"Could not find '{PREPROCESS_FILE_FUNCTION_NAME}' function in '{script}'"
        raise ValueError(message)

    logger.debug(f"Loaded file preprocessing function from '{script}'")

    return preprocess_func
