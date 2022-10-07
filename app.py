import streamlit as st
from src.keboola.connect import add_keboola_table_selection
from src.interactive_table import interactive_table

st.image('static/keboola_logo.png', width=400)

# Web App Title
st.markdown('''
# **Keboola Table Streamlit App**
---
''')

# Adds a table selection form to the sidebar of streamlit
add_keboola_table_selection()

st.subheader('Interactive Table')
st.write(
    "This is a simple table app that uses the Keboola Storage API to get the data from the selected table."
)
if "uploaded_file" in st.session_state:
    interactive_table()
