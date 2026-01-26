"""
Cook County Rental Search
Housing Authority of Cook County (HACC)
"""

import streamlit as st

st.set_page_config(
    page_title="Cook County Rental Search",
    page_icon="🏠",
    layout="wide"
)

from search_utils import render_county_page

render_county_page("cook")
