# Import libraries needed
import pandas as pd 
import streamlit as st 
import random
import base64
from streamlit_option_menu import option_menu
from pages import home, search, about, contact, details
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
def load_local_css(file_name):
    with open(file_name) as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


st.set_page_config(page_title='CreuseFix',layout="wide",initial_sidebar_state='collapsed')

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img_base64 = get_base64_image("images/CREUSEFIX__3.png")
st.markdown(f"""
    <div class="navbar">
<img src="data:image/png;base64,{img_base64}" alt="Logo" width="200" height="200">
<a href="/?page=Home">Home</a>
<a href="/?page=Search">Search</a>
<a href="/?page=Details">Details</a>
<a href="/?page=About">About</a>
<a href="/?page=Contact">Contact</a>
</div>
""", unsafe_allow_html=True)
load_local_css("assets/style.css")


actors_df = pd.read_csv("Intervenants.csv")
films = pd.read_csv('TMDb_IMDb_full.csv')

# Get page parameters
page = st.query_params.get("page", "Home")

# Page switching
if page == "Home":
    home.show_home()
if page == "Search":
    search.show_search()
elif page == "About":
    about.show_about()
elif page == "Contact":
    contact.show_contact()
elif page == "Details":
    details.show_details()
# else:
#     st.error("Page not found.")
