from importlib import metadata
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROJECT_VERSION = metadata.version("mathematicon")
