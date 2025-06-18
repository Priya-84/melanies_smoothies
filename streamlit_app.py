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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe.toPandas().to_dict('records'),  # ✅ FIX 1: Convert to list of dicts
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen['name'] + ' '                    # ✅ FIX 2: Use dict key
        st.subheader(fruit_chosen['name'] + ' Nutrition Information')      # ✅ FIX 2: Use dict key
        st.json(fruit_chosen)                                              # ✅ FIX 2: Display full JSON

my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER)
               VALUES ('""" + ingredients_string + """','""" + NAME_ON_ORDER + """')"""

st.write(my_insert_stmt)

time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, Vaanya!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.json(smoothiefroot_response.json())   # ✅ FIX 3: Proper Streamlit JSON display
