"""
HUD-VASH Rental Search Tool - Illinois
Landing page with county selection
"""

import streamlit as st
import requests
import urllib.parse
from payment_standards import (
    get_payment_standard,
    get_all_counties,
    get_all_towns,
    get_all_zip_codes,
    resolve_location
)

# Page configuration
st.set_page_config(
    page_title="HUD-VASH Rental Search - Illinois",
    page_icon="🏠",
    layout="wide"
)

# Title
st.title("HUD-VASH Rental Search")
st.markdown("**Illinois** - Find affordable rentals within Housing Authority payment standards")

st.markdown("---")

# Introduction
st.markdown("""
This tool helps HUD-VASH case managers find rental listings that fall within
Housing Authority payment standards. Select your county below to begin searching.
""")

st.markdown("### Select Your County")

# Get all counties
counties = get_all_counties()

# Create cards for each county
cols = st.columns(2)

for i, county in enumerate(counties):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(county['name'])
            st.markdown(f"**{county['authority']}**")
            st.caption(f"Effective: {county['effective_date']}")

            # Stats
            num_towns = len(get_all_towns(county['key']))
            num_zips = len(get_all_zip_codes(county['key']))
            st.markdown(f"📍 {num_towns} towns | 📮 {num_zips} ZIP codes")

            # Link to county page
            st.page_link(
                f"pages/{county['url_slug']}.py",
                label=f"Search {county['name']}",
                icon="🔍",
                use_container_width=True
            )

st.markdown("---")

# How it works
st.markdown("### How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**1. Select County**")
    st.markdown("Choose the county where your client wants to live. Each county has different payment standards.")

with col2:
    st.markdown("**2. Search Listings**")
    st.markdown("Select town or ZIP code and bedroom size. The tool searches for rentals within payment standards.")

with col3:
    st.markdown("**3. View Results**")
    st.markdown("Browse affordable listings with contact info, photos, and links to Zillow and Google Maps.")

st.markdown("### About Payment Standards")
st.markdown("""
Payment standards determine the maximum rent HUD will subsidize:

- **Location**: Different ZIP codes have different standards
- **Bedroom Size**: Larger units have higher standards
- **Housing Authority**: Each county's HA sets their own standards (90-110% of FMR)

**The "Lesser Of" Rule**: If a tenant rents a unit larger than their voucher size,
the payment standard is capped at their voucher's bedroom size. For example, a
1-bedroom voucher holder renting a 2-bedroom unit receives the 1-bedroom payment standard.

**Note**: Payment standards are updated annually, typically in January. Always verify
current standards with the Housing Authority.
""")

# Footer
st.markdown("---")
st.caption(
    "Data from RentCast API. Payment standards from local Housing Authorities. "
    "For HUD-VASH case managers helping veterans find housing."
)
