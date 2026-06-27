from validators import normalize_ingredient_name


def convert_to_base_unit(quantity, unit):
    """
    Convert quantity to base unit.
    Returns tuple: (converted_quantity, base_unit_name)
    Base units: g (grams), ml (milliliters), pcs (pieces)
    """
    if unit == "kg":
        return quantity * 1000, "g"
    elif unit == "g":
        return quantity, "g"
    elif unit == "L":
        return quantity * 1000, "ml"
    elif unit == "ml":
        return quantity, "ml"
    elif unit == "pcs":
        return quantity, "pcs"
    else:
        raise ValueError(f"Unknown unit: {unit}")


def get_unit_type(unit):
    """Return unit type: 'weight', 'volume', or 'piece'."""
    if unit in ("g", "kg"):
        return "weight"
    elif unit in ("ml", "L"):
        return "volume"
    elif unit == "pcs":
        return "piece"
    else:
        raise ValueError(f"Unknown unit: {unit}")


def can_cook_recipe(recipe, pantry):
    """
    Check if recipe can be cooked with available pantry items.

    Returns tuple: (is_cookable: bool, missing_items: list)
    missing_items is a list of dicts: {"name": str, "required": float, "available": float, "unit": str}
    """
    missing_items = []

    # Build a normalized pantry lookup: name -> {quantity, unit}
    pantry_dict = {}
    for item in pantry:
        norm_name = normalize_ingredient_name(item["name"])
        pantry_dict[norm_name] = {
            "quantity": item["quantity"],
            "unit": item["unit"]
        }

    # Check each recipe ingredient
    for ingredient in recipe.get("ingredients", []):
        req_name = normalize_ingredient_name(ingredient["name"])
        req_quantity = ingredient["quantity"]
        req_unit = ingredient["unit"]

        # Find matching pantry item
        if req_name not in pantry_dict:
            missing_items.append({
                "name": ingredient["name"],
                "required": req_quantity,
                "available": 0,
                "unit": req_unit
            })
            continue

        pantry_item = pantry_dict[req_name]
        pantry_quantity = pantry_item["quantity"]
        pantry_unit = pantry_item["unit"]

        # Check unit type compatibility
        req_unit_type = get_unit_type(req_unit)
        pantry_unit_type = get_unit_type(pantry_unit)

        if req_unit_type != pantry_unit_type:
            # Unit type mismatch: treat as missing
            missing_items.append({
                "name": ingredient["name"],
                "required": req_quantity,
                "available": pantry_quantity,
                "unit": req_unit
            })
            continue

        # Convert both to base unit for comparison
        req_base_qty, _ = convert_to_base_unit(req_quantity, req_unit)
        pantry_base_qty, _ = convert_to_base_unit(pantry_quantity, pantry_unit)

        # Check if quantity is sufficient
        if pantry_base_qty < req_base_qty:
            missing_items.append({
                "name": ingredient["name"],
                "required": req_quantity,
                "available": pantry_quantity,
                "unit": req_unit
            })

    is_cookable = len(missing_items) == 0
    return is_cookable, missing_items


def get_all_suggestions(pantry, recipes):
    """
    Generate cooking suggestions based on pantry and recipes.

    Returns dict:
    {
        "cookable": [recipe_names],
        "almost_cookable": [
            {
                "recipe_name": str,
                "missing": [{"name": str, "required": float, "available": float, "unit": str}, ...]
            },
            ...
        ]
    }
    """
    cookable = []
    almost_cookable = []

    for recipe in recipes:
        is_cookable, missing_items = can_cook_recipe(recipe, pantry)
        if is_cookable:
            cookable.append(recipe.get("recipe_name", "Unknown"))
        else:
            almost_cookable.append({
                "recipe_name": recipe.get("recipe_name", "Unknown"),
                "missing": missing_items
            })

    return {
        "cookable": cookable,
        "almost_cookable": almost_cookable
    }
