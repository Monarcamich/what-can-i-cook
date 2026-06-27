VALID_UNITS = {"g", "kg", "ml", "L", "pcs"}


def normalize_ingredient_name(name):
    """Normalize ingredient name: lowercase and strip whitespace."""
    if not isinstance(name, str):
        raise ValueError("Ingredient name must be a string")
    normalized = name.lower().strip()
    if not normalized:
        raise ValueError("Ingredient name cannot be empty")
    return normalized


def validate_unit(unit):
    """Validate that unit is in the supported set."""
    if unit not in VALID_UNITS:
        raise ValueError(f"Invalid unit '{unit}'. Must be one of: {', '.join(sorted(VALID_UNITS))}")
    return unit


def validate_quantity(quantity):
    """Validate that quantity is a positive number."""
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a number")
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")
    return qty
