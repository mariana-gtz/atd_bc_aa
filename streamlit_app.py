import os
import sys
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cwd)
from config.constants import *

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

######## Load custom CSS file ##########################################

def load_css(file_path):
    with open(file_path, "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


css_path = os.path.join(cwd, ASSETS_PATH, "styles.css")
load_css(css_path)

####### IMAGE TRANSFORMATIONS ###########################################
img_lg_path = os.path.join(cwd, ASSETS_PATH, LARGE_IMAGE_NAME)
img_sm_path = os.path.join(cwd, ASSETS_PATH, SMALL_IMAGE_NAME)

with open(img_sm_path, "rb") as f:
    image_bytes_small = f.read()

with open(img_lg_path, "rb") as f:
    image_bytes_large = f.read()


# ------- PAGE SETUP ------------

home_page = st.Page(
    page    = "views/home.py",
    title   = "Home",
    icon    = ":material/home:",
    default = True    
)
summary_page = st.Page(
    page    = "views/atd_view.py",
    title   = "ATD Overview",
    icon    = ":material/acute:",
    default = False    
)

# ------- NAVIGATION SETUP [WITH SECTIONS] ------------
pg = st.navigation(
    {   
        "Get Started": [home_page],
        "Actual Time of Delivery": [summary_page],
    }
)

# ------- SHARED ON ALL PAGES ------------
st.logo(
        image      = image_bytes_large, 
        size       = "large", 
        icon_image = image_bytes_small, 
        link       = None
       )

st.sidebar.text("Made with 🫶 for UberEats LatAm A&A Team.")


# ------- RUN NAVIGATION ------------
pg.run()