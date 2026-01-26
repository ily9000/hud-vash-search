"""
Lake County Rental Search
Lake County Housing Authority (LCHA)
"""

import streamlit as st

st.set_page_config(
    page_title="Lake County Rental Search",
    page_icon="🏠",
    layout="wide"
)

from search_utils import render_county_page

render_county_page("lake")
