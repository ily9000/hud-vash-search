"""
Shared search utilities for county pages.
"""

import streamlit as st
import requests
import urllib.parse
from payment_standards import (
    get_county_info,
    get_payment_standard,
    get_all_towns,
    resolve_location
)


def get_api_key():
    """Get RentCast API key from Streamlit secrets."""
    try:
        return st.secrets["RENTCAST_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def search_rentals(zip_code: str, api_key: str, bedrooms: int | None = None) -> list[dict]:
    """Search RentCast API for rental listings."""
    url = "https://api.rentcast.io/v1/listings/rental/long-term"

    headers = {
        "Accept": "application/json",
        "X-Api-Key": api_key
    }

    params = {
        "zipCode": zip_code,
        "status": "Active",
        "limit": 50
    }

    if bedrooms is not None:
        params["bedrooms"] = bedrooms

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return []


def format_price(price: int | float | None) -> str:
    """Format price as currency string."""
    if price is None:
        return "Price not listed"
    return f"${price:,.0f}/mo"


def render_county_page(county_key: str):
    """Render a complete county search page."""
    county = get_county_info(county_key)
    if not county:
        st.error("County not found")
        return

    # Page title
    st.title(f"HUD-VASH Rental Search")
    st.markdown(f"**{county['name']}** - Search rentals within {county['authority']} payment standards")

    # Show payment standards explainer in an expander
    with st.expander("How Payment Standards Work in This County", expanded=False):
        st.markdown(county['explainer'])
        st.caption(f"Effective: {county['effective_date']}")

    st.markdown("---")

    # Sidebar with search form
    with st.sidebar:
        st.header("Search Criteria")

        # Bedroom options
        bedroom_options = {
            "Studio": 0,
            "1 Bedroom": 1,
            "2 Bedroom": 2,
            "3 Bedroom": 3,
            "4 Bedroom": 4
        }
        bedroom_labels = list(bedroom_options.keys())

        voucher_label = st.selectbox(
            "Voucher Bedroom Size",
            options=bedroom_labels,
            index=1,
            help="The voucher entitlement size (used for payment standard calculation)"
        )
        voucher_bedrooms = bedroom_options[voucher_label]

        search_bedroom_labels = st.multiselect(
            "Unit Sizes to Search",
            options=bedroom_labels,
            default=[voucher_label],
            help="Which unit sizes to search for (can select multiple)"
        )
        search_bedrooms = [bedroom_options[label] for label in search_bedroom_labels]

        # Town selector
        all_towns = get_all_towns(county_key)

        selected_towns = st.multiselect(
            "Select Towns",
            options=all_towns,
            placeholder="Type to search towns...",
            help="Start typing to filter towns, then click to select"
        )

        extra_zips = st.text_input(
            "Additional ZIP Codes (optional)",
            placeholder="60601, 60602",
            help="Add specific ZIP codes not covered by town selection"
        )

        location_input = ", ".join(selected_towns)
        if extra_zips:
            location_input = f"{location_input}, {extra_zips}" if location_input else extra_zips

        search_clicked = st.button("Search Rentals", type="primary", use_container_width=True)

        st.markdown("---")
        st.markdown(f"**{county['authority']}**")
        st.caption(f"Effective: {county['effective_date']}")
        st.caption(f"{len(all_towns)} towns available")

        # Link back to home
        st.markdown("---")
        st.page_link("app.py", label="Change County", icon="🔄")

    # Main content
    api_key = get_api_key()

    if not api_key:
        st.warning(
            "**API Key Not Configured**\n\n"
            "To use this app, add your RentCast API key:\n"
            "1. Sign up at [rentcast.io](https://rentcast.io)\n"
            "2. In Streamlit Cloud: Settings -> Secrets -> Add `RENTCAST_API_KEY`\n"
            "3. For local testing: Create `.streamlit/secrets.toml` with:\n"
            "   ```\n"
            '   RENTCAST_API_KEY = "your-api-key-here"\n'
            "   ```"
        )

    if search_clicked and location_input:
        locations = [loc.strip() for loc in location_input.split(",") if loc.strip()]

        if not locations:
            st.error("Please enter at least one town or ZIP code")
        elif not api_key:
            st.error("API key not configured. See instructions above.")
        else:
            all_zips = []
            unresolved = []

            for loc in locations:
                zips = resolve_location(county_key, loc)
                if zips:
                    all_zips.extend(zips)
                else:
                    unresolved.append(loc)

            valid_zips = list(dict.fromkeys(all_zips))

            if unresolved:
                st.warning(f"Could not find: {', '.join(unresolved)}")

            if valid_zips:
                st.info(f"Searching {len(valid_zips)} ZIP codes: {', '.join(valid_zips[:10])}{'...' if len(valid_zips) > 10 else ''}")

                # Show payment standards
                st.subheader(f"Payment Standards ({voucher_label} Voucher)")
                display_zips = valid_zips[:8]
                cols = st.columns(min(len(display_zips), 4))
                for i, zip_code in enumerate(display_zips):
                    payment_std = get_payment_standard(county_key, zip_code, voucher_bedrooms)
                    with cols[i % 4]:
                        st.metric(
                            label=f"ZIP {zip_code}",
                            value=f"${payment_std:,}" if payment_std else "N/A"
                        )

                st.markdown("---")

                # Search listings
                all_listings = []
                progress_bar = st.progress(0)
                status_text = st.empty()

                for i, zip_code in enumerate(valid_zips):
                    status_text.text(f"Searching {zip_code}...")
                    progress_bar.progress((i + 1) / len(valid_zips))

                    listings = search_rentals(zip_code, api_key)

                    for listing in listings:
                        listing["_search_zip"] = zip_code
                        listing_bedrooms = listing.get("bedrooms", 0) or 0
                        effective_bedrooms = min(listing_bedrooms, voucher_bedrooms)
                        listing["_payment_standard"] = get_payment_standard(county_key, zip_code, effective_bedrooms)

                    all_listings.extend(listings)

                progress_bar.empty()
                status_text.empty()

                if not all_listings:
                    st.info("No rentals found in the selected areas.")
                else:
                    if search_bedrooms:
                        all_listings = [
                            listing for listing in all_listings
                            if (listing.get("bedrooms", 0) or 0) in search_bedrooms
                        ]

                    affordable_listings = []
                    for listing in all_listings:
                        price = listing.get("price")
                        payment_std = listing.get("_payment_standard")
                        is_affordable = (price is None or payment_std is None or payment_std == 0 or price <= payment_std)
                        if is_affordable:
                            affordable_listings.append(listing)

                    affordable_listings.sort(key=lambda x: x.get("price") or 0)

                    st.success(f"Found {len(affordable_listings)} affordable listings within payment standard.")

                    st.subheader(f"Affordable Listings ({len(affordable_listings)})")

                    if affordable_listings:
                        for listing in affordable_listings:
                            address = listing.get("formattedAddress", "Address not available")
                            price = listing.get("price")
                            payment_std = listing.get("_payment_standard")
                            sqft = listing.get("squareFootage")
                            listing_br = listing.get("bedrooms", 0) or 0

                            br_display = "Studio" if listing_br == 0 else f"{listing_br} BR"

                            with st.container():
                                col1, col2, col3 = st.columns([3, 1.5, 1])

                                with col1:
                                    st.markdown(f"**{address}**")
                                    details = [br_display]
                                    if sqft:
                                        details.append(f"{sqft:,} sq ft")
                                    if listing.get("propertyType"):
                                        details.append(listing.get("propertyType"))
                                    st.caption(" | ".join(details))

                                with col2:
                                    st.markdown(f"**{format_price(price)}**")
                                    if price and payment_std:
                                        savings = payment_std - price
                                        if savings > 0:
                                            st.caption(f"${savings:,} under limit")

                                with col3:
                                    google_query = urllib.parse.quote(f"{address} rental")
                                    google_url = f"https://www.google.com/search?q={google_query}"
                                    st.link_button("Search Google", google_url, use_container_width=True)

                                st.markdown("---")
                    else:
                        st.info("No affordable listings found matching your criteria.")
            else:
                st.error(f"No valid locations found in {county['name']}. Try entering town names or ZIP codes.")

    elif search_clicked and not location_input:
        st.error("Please select at least one town or enter a ZIP code")

    elif not search_clicked and api_key:
        st.info(
            "**Get Started:** Select your voucher size and towns in the sidebar, "
            "then click **Search Rentals** to find affordable listings."
        )

    # Footer
    st.markdown("---")
    st.caption(
        f"Data from RentCast API. Payment standards from {county['authority']}, "
        f"effective {county['effective_date']}. For HUD-VASH case managers."
    )
