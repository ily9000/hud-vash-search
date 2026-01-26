"""
Housing Voucher Rental Search Tool - Illinois
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
    page_title="Housing Voucher Rental Search - Illinois",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
    }

    /* Info boxes */
    .info-box {
        background-color: #f0f7ff;
        border-left: 4px solid #1e3a5f;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }

    /* Step cards */
    .step-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        height: 100%;
    }
    .step-number {
        background: #1e3a5f;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    /* Glossary terms */
    .glossary-term {
        background: #fff8e6;
        border-left: 3px solid #ffc107;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
    }
    .glossary-term strong {
        color: #1e3a5f;
    }

    /* Better button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }

    /* County card improvements */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 10px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="main-header">
    <h1>🏠 Housing Voucher Rental Search</h1>
    <p style="font-size: 1.2rem; margin: 0;">Find affordable rentals for Housing Choice Voucher holders in Illinois</p>
</div>
""", unsafe_allow_html=True)

# Welcome message with plain language
st.markdown("""
<div class="info-box">
    <strong>👋 Welcome!</strong><br>
    This tool helps case managers and voucher holders quickly find rental listings that fit
    within Housing Choice Voucher (Section 8) payment standards. No more manual searching
    across multiple websites or calculating payment standards by hand.
</div>
""", unsafe_allow_html=True)

st.markdown("### Step 1: Select Your County")
st.markdown("Each county has its own Housing Authority with different rent limits. Pick where your client wants to live.")

# Get all counties
counties = get_all_counties()

# Create cards for each county
cols = st.columns(2)

for i, county in enumerate(counties):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(county['name'])
            st.caption(county['authority'])

            # Stats with clearer labels
            num_towns = len(get_all_towns(county['key']))
            num_zips = len(get_all_zip_codes(county['key']))
            st.markdown(f"**{num_towns}** towns  •  **{num_zips}** ZIP codes")
            st.caption(f"Standards updated: {county['effective_date']}")

            # Link to official payment standards
            if county.get('payment_standards_url'):
                st.markdown(f"[📄 View official payment standards]({county['payment_standards_url']})")

            # Link to county page
            if st.button(f"Search {county['name']}", key=f"btn_{county['key']}", type="primary", use_container_width=True):
                st.switch_page(f"pages/{county['url_slug']}.py")

st.markdown("---")

# What happens next
st.markdown("### What Happens Next")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### Step 2: Enter Search Details")
        st.markdown("Choose the voucher bedroom size and select towns or ZIP codes to search.")

with col2:
    with st.container(border=True):
        st.markdown("#### Step 3: Review Listings")
        st.markdown("See only rentals your client can afford. Click to view details and contact landlords.")

st.markdown("---")

# Glossary section - key terms explained in plain language
st.markdown("### 📖 Key Terms Explained")
st.markdown("*Understanding the basics of housing vouchers*")

with st.expander("**What is a Payment Standard?** (Click to expand)", expanded=False):
    st.markdown("""
    **In simple terms:** The payment standard is the **maximum rent amount** that HUD will help pay for a unit.

    Think of it as a rent ceiling:
    - If a rental costs **less** than the payment standard → Your client can afford it ✅
    - If a rental costs **more** than the payment standard → Your client pays the difference out of pocket

    **Why does it vary?**
    - 📍 **Location:** Rent limits differ by ZIP code (higher in expensive areas)
    - 🛏️ **Bedroom size:** Larger units have higher limits
    - 🏛️ **Housing Authority:** Each county sets their own standards
    """)

with st.expander("**What is the 'Lesser Of' Rule?**", expanded=False):
    st.markdown("""
    **The short version:** If your client rents a unit **bigger** than their voucher size, HUD only pays based on their voucher size.

    **Example:**
    - Sarah has a **1-bedroom voucher** (entitled to $1,200 payment standard)
    - She finds a nice **2-bedroom apartment** for $1,100/month
    - Even though the 2-BR payment standard is $1,500, HUD uses the **1-BR limit of $1,200**
    - Since $1,100 < $1,200, Sarah can afford this unit! ✅

    **Why this matters for your search:**
    This tool automatically handles this calculation. When you set the voucher size,
    it uses that limit even when searching for larger units.
    """)

with st.expander("**What voucher types does this tool support?**", expanded=False):
    st.markdown("""
    This tool works for **all Housing Choice Voucher (Section 8) programs**, including:

    - 🏠 **Standard HCV** - Traditional Section 8 vouchers
    - 🎖️ **HUD-VASH** - Veterans Affairs Supportive Housing for homeless veterans
    - 👨‍👩‍👧 **Family Unification Program (FUP)** - For families in child welfare system
    - 🏢 **Project-Based Vouchers** - Tied to specific properties
    - 🦽 **Mainstream Vouchers** - For non-elderly people with disabilities

    The payment standards are the same across all voucher types within each Housing Authority.
    """)

# Pro tips
st.markdown("---")
st.markdown("### 💡 Tips for Your Search")

tip_col1, tip_col2 = st.columns(2)

with tip_col1:
    with st.container(border=True):
        st.markdown("**Before Your Search**")
        st.markdown("""
        - Confirm the voucher bedroom size
        - Know which areas are preferred or accessible
        - Have the move-in budget ready to discuss
        """)

with tip_col2:
    with st.container(border=True):
        st.markdown("**After Finding Listings**")
        st.markdown("""
        - Call landlords to verify availability
        - Ask about HCV/VASH acceptance upfront
        - Schedule viewings quickly (rentals move fast!)
        """)

# Footer
st.markdown("---")
st.caption(
    "Data from RentCast API. Payment standards from local Housing Authorities. "
    "Built to help Housing Choice Voucher holders find affordable rentals. "
    "Always verify current payment standards with your Housing Authority."
)
