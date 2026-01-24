"""
DuPage County HUD-VASH Rental Search
DuPage Housing Authority (DHA)
"""

import streamlit as st

st.set_page_config(
    page_title="DuPage County HUD-VASH Rental Search",
    page_icon="🏠",
    layout="wide"
)

from search_utils import render_county_page

render_county_page("dupage")
