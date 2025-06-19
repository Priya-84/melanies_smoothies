# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col, lower, lit
import pandas as pd

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Name input
NAME_ON_ORDER = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be:', NAME_ON_ORDER)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options from Snowflake (FRUIT_NAME + SEARCH_ON)
fruit_df = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"), col("SEARCH_ON")
).to_pandas()

# Dropdown options
fruit_options = fruit_df["FRUIT_NAME"].tolist()

# Multiselect box
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    options=fruit_options,
    max_selections=5
)

# Build smoothie string and display nutrition info
ingredients_string = ""
if ingredients_list:
    for fruit_name in ingredients_list:
        ingredients_string += fruit_name + " "

        # Get corresponding search_on value from fruit_df
        search_on = fruit_df.loc[fruit_df["FRUIT_NAME"] == fruit_name, "SEARCH_ON"].values[0]

        st.subheader(f"{fruit_name} Nutrition Information")

        # Fetch matching rows from smoothiefroot_data table
        nutrition_data = session.table("smoothies.public.smoothiefroot_data") \
            .filter(lower(col("NAME")) == lit(search_on.lower())) \
            .to_pandas()

        # Show result in table
        st.dataframe(nutrition_data, use_container_width=True)

# Prepare SQL insert
my_insert_stmt = f"""
INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER)
VALUES ('{ingredients_string.strip()}', '{NAME_ON_ORDER}')
"""

# Show the insert statement
st.write(my_insert_stmt)

# Submit button
if st.button("Submit Order"):
    session.sql(my_insert_stmt).collect()
    st.success(f"Your Smoothie is ordered, {'Vaanya'}!", icon="✅")
