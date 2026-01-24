"""
Will County HUD-VASH Rental Search
Housing Authority of Joliet (HAJ)
"""

import streamlit as st

st.set_page_config(
    page_title="Will County HUD-VASH Rental Search",
    page_icon="🏠",
    layout="wide"
)

from search_utils import render_county_page

render_county_page("will")
