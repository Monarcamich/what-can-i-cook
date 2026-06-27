# What Can I Cook? 🍳

A Python + Streamlit application for managing your pantry and discovering what recipes you can cook with available ingredients.

## Features

- **Pantry Management**: Add and track ingredients with quantities, units, and expiration dates
- **Recipe Management**: Store recipes with their required ingredients
- **Smart Suggestions**: Get real-time suggestions on what you can cook
  -  **COOKABLE**: Recipes you can make right now
  -  **ALMOST_COOKABLE**: Recipes missing a few ingredients (shows exactly what's needed)

## Technical Details

### Supported Units
- **Weight**: grams (g), kilograms (kg)
- **Volume**: milliliters (ml), liters (L)
- **Pieces**: pieces (pcs)

### Unit Conversion
The app automatically converts between compatible units:
- 1 kg = 1000 g
- 1 L = 1000 ml
- Different unit types (e.g., grams vs. pieces) are detected and handled gracefully

### Data Storage
- Pantry and recipes are stored locally as JSON files in the `data/` directory
- No internet connection required
- Data persists between sessions

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone/navigate to the project directory**
   ```bash
   cd what-can-i-cook
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage Guide

### Tab 1: Pantry
- **Add items**: Enter ingredient name, quantity, unit, and optional expiration date
- **View inventory**: See all stored items in a table format
- **Update items**: Adding an item with the same name updates its quantity/unit
- **Clear all**: Remove all pantry items at once

### Tab 2: Recipes
- **Add recipes**: Enter recipe name and at least one ingredient
- **Multiple ingredients**: Use the provided fields to add up to 5 ingredients per recipe
- **View recipes**: See all saved recipes in an expandable list
- **Clear all**: Remove all recipes at once

### Tab 3: Suggestions
- **Generate suggestions**: Click the button to see what you can cook
- **Results**: 
  -  Recipes you have all ingredients for (with sufficient quantities)
  -  Recipes missing some ingredients (shows exactly what's needed and how much)

## Example Workflow

1. **Add pantry items**:
   - Eggs: 6 pcs
   - Butter: 100 g
   - Milk: 500 ml

2. **Add a recipe**:
   - Recipe: "French Omelette"
   - Ingredients:
     - Eggs: 3 pcs
     - Butter: 30 g
     - Milk: 100 ml

3. **Generate suggestions**: Click "Generate Suggestions" to see that "French Omelette" is cookable!

## Project Structure

```
what-can-i-cook/
├── app.py              # Streamlit UI (3 tabs: Pantry, Recipes, Suggestions)
├── validators.py       # Input validation & normalization
├── storage.py          # JSON file I/O
├── logic.py            # Unit conversion & recipe matching
├── requirements.txt    # Python dependencies
├── data/
│   ├── pantry.json     # Stored pantry items
│   └── recipes.json    # Stored recipes
└── README.md          # This file
```

## Data Format

### pantry.json
```json
[
  {
    "name": "eggs",
    "quantity": 6,
    "unit": "pcs",
    "expiration_date": "2026-06-15"
  }
]
```

### recipes.json
```json
[
  {
    "recipe_name": "omelette",
    "ingredients": [
      {"name": "eggs", "quantity": 3, "unit": "pcs"},
      {"name": "butter", "quantity": 30, "unit": "g"}
    ]
  }
]
```

## Validation Rules

- **Ingredient names**: Normalized to lowercase; whitespace is trimmed
- **Quantities**: Must be positive numbers
- **Units**: Must be one of the supported units (g, kg, ml, L, pcs)
- **Recipes**: Must have at least one ingredient
- **Unit mismatches**: If pantry item and recipe ingredient have incompatible units (e.g., pcs vs. g), the ingredient is treated as missing

## Error Handling

The app gracefully handles:
- Empty ingredient names
- Invalid quantities (zero or negative)
- Invalid units
- Recipes with no ingredients
- Unit type mismatches
- Missing or corrupted JSON files (resets to empty)

## Future Enhancements (Beyond MVP)

- Expiration date tracking with visual alerts
- Recipe search and filtering
- Shopping list generation (suggested ingredients to buy)
- Category tagging for ingredients
- Dietary restrictions and preferences
- User ratings for recipes

## License

This is a personal project for educational purposes.
