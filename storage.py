import json
import os

PANTRY_FILE = "data/pantry.json"
RECIPES_FILE = "data/recipes.json"


def _ensure_data_dir():
    """Ensure data directory exists."""
    os.makedirs("data", exist_ok=True)


def load_pantry():
    """Load pantry from JSON file. Return empty list if file doesn't exist."""
    _ensure_data_dir()
    if not os.path.exists(PANTRY_FILE):
        return []
    try:
        with open(PANTRY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_pantry(pantry_list):
    """Save pantry list to JSON file."""
    _ensure_data_dir()
    with open(PANTRY_FILE, "w") as f:
        json.dump(pantry_list, f, indent=2)


def load_recipes():
    """Load recipes from JSON file. Return empty list if file doesn't exist."""
    _ensure_data_dir()
    if not os.path.exists(RECIPES_FILE):
        return []
    try:
        with open(RECIPES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_recipes(recipes_list):
    """Save recipes list to JSON file."""
    _ensure_data_dir()
    with open(RECIPES_FILE, "w") as f:
        json.dump(recipes_list, f, indent=2)
