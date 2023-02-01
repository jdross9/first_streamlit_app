import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError  ## Handles error message handling

streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach, & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled, Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

## New section to display fruityvice api reponse
streamlit.header("Fruityvice Fruit Advice!")
#fruit_choice = streamlit.text_input('What fruit would you like information about?')
##fruit_choice = streamlit.text_input('What fruit would you like information about?','kiwi')
##streamlit.write('The user entered ', fruit_choice)
#
## import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
###streamlit.text(fruityvice_response.json())
#
## Take the json response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
## output to screen as a table
#streamlit.dataframe(fruityvice_normalized)
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
    
except URLError as e:
  streamlit.error()
    
# don't run anything past here while we troubleshoot
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
##my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
#my_data_row = my_cur.fetchone() ## Just to fetch one
my_data_rows = my_cur.fetchall()
#streamlit.text("The fruit load list contains:")
streamlit.header("The fruit load list contains:")
## Below line printed ('JROSS', 'JI02638', 'AWS_CA_CENTRAL_1')
#streamlit.text(my_data_row)
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','cantaloupe')
streamlit.write('Thanks for adding ', add_my_fruit)

# This will not work correctly but go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
