"""
HUD-VASH Rental Search Tool - Illinois
Landing page with county selection
"""

import streamlit as st
from payment_standards import get_all_counties, get_all_towns, get_all_zip_codes

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

                if affordable_listings:
                    for listing in affordable_listings:
                        address = listing.get("formattedAddress", "Address not available")
                        price = listing.get("price")
                        payment_std = listing.get("_payment_standard")
                        sqft = listing.get("squareFootage")
                        listing_br = listing.get("bedrooms", 0) or 0
                        bathrooms = listing.get("bathrooms")
                        year_built = listing.get("yearBuilt")
                        lot_size = listing.get("lotSize")
                        property_type = listing.get("propertyType")
                        days_on_market = listing.get("daysOnMarket")
                        listed_date = listing.get("listedDate")
                        listing_agent = listing.get("listingAgent") or {}
                        listing_office = listing.get("listingOffice") or {}

with col1:
    st.markdown("**1. Select County**")
    st.markdown("Choose the county where your client wants to live. Each county has different payment standards.")

                        with st.container():
                            # Header row: Address and Price
                            header_col1, header_col2 = st.columns([3, 1])

                            with header_col1:
                                st.markdown(f"### {address}")

                            with header_col2:
                                st.markdown(f"### {format_price(price)}")
                                if price and payment_std:
                                    savings = payment_std - price
                                    if savings > 0:
                                        st.caption(f":green[${savings:,} under limit]")

                            # Property details row
                            detail_cols = st.columns(6)

                            with detail_cols[0]:
                                st.metric("Bedrooms", br_display)

                            with detail_cols[1]:
                                bath_display = f"{bathrooms}" if bathrooms else "—"
                                st.metric("Bathrooms", bath_display)

                            with detail_cols[2]:
                                sqft_display = f"{sqft:,}" if sqft else "—"
                                st.metric("Sq Ft", sqft_display)

                            with detail_cols[3]:
                                year_display = str(year_built) if year_built else "—"
                                st.metric("Year Built", year_display)

                            with detail_cols[4]:
                                type_display = property_type if property_type else "—"
                                st.metric("Type", type_display)

                            with detail_cols[5]:
                                days_display = f"{days_on_market}" if days_on_market else "—"
                                st.metric("Days Listed", days_display)

                            # Expandable section for more details
                            with st.expander("More Details & Contact Info"):
                                info_col1, info_col2, info_col3 = st.columns(3)

                                with info_col1:
                                    st.markdown("**Listing Info**")
                                    if listed_date:
                                        st.write(f"Listed: {listed_date[:10] if len(listed_date) > 10 else listed_date}")
                                    if lot_size:
                                        st.write(f"Lot Size: {lot_size:,} sq ft")
                                    if payment_std:
                                        st.write(f"Payment Standard: ${payment_std:,}")
                                    mls_number = listing.get("mlsNumber")
                                    mls_name = listing.get("mlsName")
                                    if mls_number:
                                        st.write(f"MLS #: {mls_number}")
                                    if mls_name:
                                        st.write(f"MLS: {mls_name}")

                                with info_col2:
                                    st.markdown("**Listing Agent**")
                                    if listing_agent.get("name"):
                                        st.write(f"{listing_agent.get('name')}")
                                    if listing_agent.get("phone"):
                                        st.write(f"Phone: {listing_agent.get('phone')}")
                                    if listing_agent.get("email"):
                                        st.write(f"Email: {listing_agent.get('email')}")
                                    if not any([listing_agent.get("name"), listing_agent.get("phone"), listing_agent.get("email")]):
                                        st.write("Not available")

                                with info_col3:
                                    st.markdown("**Listing Office**")
                                    if listing_office.get("name"):
                                        st.write(f"{listing_office.get('name')}")
                                    if listing_office.get("phone"):
                                        st.write(f"Phone: {listing_office.get('phone')}")
                                    if listing_office.get("email"):
                                        st.write(f"Email: {listing_office.get('email')}")
                                    if not any([listing_office.get("name"), listing_office.get("phone"), listing_office.get("email")]):
                                        st.write("Not available")

                            # Links row
                            link_col1, link_col2, link_col3, link_col4 = st.columns(4)

                            # Build search-friendly address formats
                            zillow_addr = address.replace(",", "").replace(" ", "-")
                            zillow_url = f"https://www.zillow.com/homes/{zillow_addr}_rb/"
                            apartments_query = urllib.parse.quote(address)
                            apartments_url = f"https://www.apartments.com/{apartments_query}/"
                            google_query = urllib.parse.quote(f"{address} for rent")
                            google_url = f"https://www.google.com/search?q={google_query}"
                            maps_query = urllib.parse.quote(address)
                            maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"

                            with link_col1:
                                st.link_button("Zillow", zillow_url, use_container_width=True)
                            with link_col2:
                                st.link_button("Apartments.com", apartments_url, use_container_width=True)
                            with link_col3:
                                st.link_button("Google Search", google_url, use_container_width=True)
                            with link_col4:
                                st.link_button("Google Maps", maps_url, use_container_width=True)

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
