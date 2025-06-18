# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """)

NAME_ON_ORDER = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be', NAME_ON_ORDER)

cnx = st.connection("snowflake")
session = cnx.session()

# ✅ Get required columns from table
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), 
    col('FRUIT_ID'), 
    col('FAMILY'), 
    col('FRUIT_ORDER')
)

# ✅ Convert Snowpark DataFrame to Pandas and rename columns to match JSON keys
df = my_dataframe.to_pandas()
df = df.rename(columns={
    'FRUIT_NAME': 'name',
    'FRUIT_ID': 'id',
    'FAMILY': 'family',
    'FRUIT_ORDER': 'order'
})

# ✅ Show original table if needed
st.dataframe(df)

# ✅ Multiselect with list of dicts
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    df.to_dict('records'),  # 👈 returns list of JSON-like dicts
    max_selections=5,
    format_func=lambda fruit: fruit["name"]  # 👈 show fruit names in dropdown
)

# ✅ Process selected ingredients
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen['name'] + ' '
        st.subheader(fruit_chosen['name'] + ' Nutrition Information')
        st.json(fruit_chosen)  # 👈 this matches your screenshot (blue box)
