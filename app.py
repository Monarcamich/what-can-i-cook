import streamlit as st #Here importing streamlit library to create the web app interface
import pandas as pd #Here importing pandas library to handle data for display the pantry and recipes.
from datetime import datetime #Here importing datatime library for handling expiration dates.

from storage import load_pantry, save_pantry, load_recipes, save_recipes #Here importing functions for read and write pantry and recipes data locally.
from validators import normalize_ingredient_name, validate_unit, validate_quantity, VALID_UNITS #Here importing functions for validate user input and normilize ingredients names.
from logic import get_all_suggestions #Here importing the logic functions to generate cooking suggestions based on pantry and recipes.

st.set_page_config(page_title="What Can I Cook?", layout="wide")#Set the title for the app layout.

if "pantry" not in st.session_state:
    st.session_state.pantry = load_pantry()

if "recipes" not in st.session_state:
    st.session_state.recipes = load_recipes()

#Title
st.title("What Can I Cook?")
st.subheader("By Raúl Antonio Arellano González")

tab1, tab2, tab3 = st.tabs(["Pantry", "Recipes", "Suggestions"])


# TAB 1: PANTRY Management
with tab1:
    st.header("Pantry Management")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ingredient_name = st.text_input(
            "Ingredient name",
            key="pantry_name",
            placeholder="e.g., eggs"
        )
    with col2:
        quantity = st.number_input(
            "Quantity",
            value=1.0,
            step=0.1,
            key="pantry_qty",
            min_value=0.1
        )
    with col3:
        unit = st.selectbox(
            "Unit",
            options=sorted(VALID_UNITS),
            key="pantry_unit"
        )
    with col4:
        expiration_date = st.date_input(
            "Expiration date (optional)",
            value=None,
            key="pantry_exp"
        )

    if st.button("Add Item", key="btn_add_pantry"):
        try:
            norm_name = normalize_ingredient_name(ingredient_name)
            validate_quantity(quantity)
            validate_unit(unit)

            # Check if item already exists, update or add
            found = False
            for item in st.session_state.pantry:
                if normalize_ingredient_name(item["name"]) == norm_name:
                    item["quantity"] = quantity
                    item["unit"] = unit
                    item["expiration_date"] = expiration_date.isoformat() if expiration_date else ""
                    found = True
                    break
            if not found:
                st.session_state.pantry.append({
                    "name": ingredient_name,
                    "quantity": quantity,
                    "unit": unit,
                    "expiration_date": expiration_date.isoformat() if expiration_date else ""
                })

            save_pantry(st.session_state.pantry)
            st.success(f"Added/Updated: {ingredient_name}")
            st.rerun()
        except ValueError as e:
            st.error(f"Error: {e}")

    st.subheader("Current Pantry")
    if st.session_state.pantry:
        pantry_display = []
        for item in st.session_state.pantry:
            pantry_display.append({
                "Ingredient": item["name"],
                "Quantity": item["quantity"],
                "Unit": item["unit"],
                "Expiration": item.get("expiration_date", "") or "—"
            })
        df = pd.DataFrame(pantry_display)
        st.dataframe(df, use_container_width=True, hide_index=True)

        if st.button("Clear All Pantry", key="btn_clear_pantry"):
            st.session_state.pantry = []
            save_pantry(st.session_state.pantry)
            st.success("Pantry cleared")
            st.rerun()
    else:
        st.info("No items in pantry yet.")

# TAB 2: RECIPES
with tab2:
    st.header("Recipe Management")

    recipe_name = st.text_input(
        "Recipe name",
        key="recipe_name",
        placeholder="e.g., omelette"
    )

    st.subheader("Ingredients (add at least 1)")
    ingredients = []
    num_ingredient_rows = 5

    cols = st.columns([2, 1, 1])
    with cols[0]:
        st.write("**Ingredient Name**")
    with cols[1]:
        st.write("**Quantity**")
    with cols[2]:
        st.write("**Unit**")

    for i in range(num_ingredient_rows):
        cols = st.columns([2, 1, 1])
        with cols[0]:
            ing_name = st.text_input(
                "Name",
                key=f"ing_name_{i}",
                label_visibility="collapsed"
            )
        with cols[1]:
            ing_qty = st.number_input(
                "Qty",
                value=0.0,
                step=0.1,
                key=f"ing_qty_{i}",
                label_visibility="collapsed",
                min_value=0.0
            )
        with cols[2]:
            ing_unit = st.selectbox(
                "Unit",
                options=sorted(VALID_UNITS),
                key=f"ing_unit_{i}",
                label_visibility="collapsed"
            )

        if ing_name and ing_qty > 0:
            ingredients.append({
                "name": ing_name,
                "quantity": ing_qty,
                "unit": ing_unit
            })

    if st.button("Add Recipe", key="btn_add_recipe"):
        try:
            if not recipe_name.strip():
                st.error("Recipe name cannot be empty")
            elif not ingredients:
                st.error("Add at least one ingredient")
            else:
                # Normalize ingredient names
                normalized_ingredients = []
                for ing in ingredients:
                    norm_ing_name = normalize_ingredient_name(ing["name"])
                    validate_quantity(ing["quantity"])
                    validate_unit(ing["unit"])
                    normalized_ingredients.append({
                        "name": ing["name"],
                        "quantity": ing["quantity"],
                        "unit": ing["unit"]
                    })

                st.session_state.recipes.append({
                    "recipe_name": recipe_name,
                    "ingredients": normalized_ingredients
                })
                save_recipes(st.session_state.recipes)
                st.success(f"Added recipe: {recipe_name}")
                st.rerun()
        except ValueError as e:
            st.error(f"Error: {e}")

    st.subheader("Saved Recipes")
    if st.session_state.recipes:
        for recipe in st.session_state.recipes:
            with st.expander(f"{recipe['recipe_name']}"):
                for ing in recipe.get("ingredients", []):
                    st.write(f"  • {ing['name']}: {ing['quantity']} {ing['unit']}")

        if st.button("Clear All Recipes", key="btn_clear_recipes"):
            st.session_state.recipes = []
            save_recipes(st.session_state.recipes)
            st.success("Recipes cleared")
            st.rerun()
    else:
        st.info("No recipes added yet.")

# TAB 3: SUGGESTIONS
with tab3:
    st.header("Cooking Suggestions")

    if st.button("🔍 Generate Suggestions", key="btn_generate"):
        if not st.session_state.pantry:
            st.warning("⚠️ Please add items to your pantry first.")
        elif not st.session_state.recipes:
            st.warning("⚠️ Please add recipes first.")
        else:
            suggestions = get_all_suggestions(st.session_state.pantry, st.session_state.recipes)

            # Cookable section
            st.subheader("✅ Cookable Now")
            if suggestions["cookable"]:
                for recipe_name in suggestions["cookable"]:
                    st.success(f"🍽️ {recipe_name}")
            else:
                st.info("No recipes can be cooked with current pantry.")

            # Almost cookable section
            st.subheader("🤔 Almost Cookable (Missing Ingredients)")
            if suggestions["almost_cookable"]:
                for item in suggestions["almost_cookable"]:
                    with st.expander(f"📖 {item['recipe_name']}"):
                        st.write("**Missing:**")
                        for missing in item["missing"]:
                            missing_qty = missing["required"] - missing["available"]
                            if missing["available"] > 0:
                                st.write(
                                    f"  • {missing['name']}: need {missing_qty:.2g} {missing['unit']} "
                                    f"(have {missing['available']:.2g})"
                                )
                            else:
                                st.write(
                                    f"  • {missing['name']}: need {missing['required']:.2g} {missing['unit']} "
                                    f"(have 0)"
                                )
            else:
                st.info("No almost-cookable recipes.")
    else:
        st.info("Click 'Generate Suggestions' to see what you can cook!")
