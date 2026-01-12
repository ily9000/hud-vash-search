"""
HUD-VASH Rental Search Tool for Cook County, IL

A Streamlit web app that searches rental listings and filters by HACC payment standards.
"""

import streamlit as st
import requests
from payment_standards import get_payment_standard, is_valid_zip

# Page configuration
st.set_page_config(
    page_title="HUD-VASH Rental Search",
    page_icon="🏠",
    layout="wide"
)

# Title
st.title("HUD-VASH Rental Search")
st.markdown("**Cook County, IL** - Search rentals within HACC payment standards")
st.markdown("---")


def get_api_key():
    """Get RentCast API key from Streamlit secrets."""
    try:
        return st.secrets["RENTCAST_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def search_rentals(zip_code: str, bedrooms: int, api_key: str) -> list[dict]:
    """
    Search RentCast API for rental listings.

    Args:
        zip_code: 5-digit ZIP code
        bedrooms: Number of bedrooms (0 for studio)
        api_key: RentCast API key

    Returns:
        List of rental listings
    """
    url = "https://api.rentcast.io/v1/listings/rental/long-term"

    headers = {
        "Accept": "application/json",
        "X-Api-Key": api_key
    }

    params = {
        "zipCode": zip_code,
        "bedrooms": bedrooms,
        "status": "Active",
        "limit": 50
    }

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


# Sidebar with search form
with st.sidebar:
    st.header("Search Criteria")

    # Bedroom selection
    bedroom_options = {
        "Studio": 0,
        "1 Bedroom": 1,
        "2 Bedroom": 2,
        "3 Bedroom": 3,
        "4 Bedroom": 4
    }
    bedroom_label = st.selectbox("Bedrooms", options=list(bedroom_options.keys()))
    bedrooms = bedroom_options[bedroom_label]

    # ZIP code input
    zip_input = st.text_input(
        "ZIP Code(s)",
        placeholder="60601, 60602, 60610",
        help="Enter one or more ZIP codes, separated by commas"
    )

    # Search button
    search_clicked = st.button("Search", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown("**Payment Standards:** HACC 2026")
    st.markdown("[RentCast API](https://rentcast.io)")


# Main content area
api_key = get_api_key()

if not api_key:
    st.warning(
        "⚠️ **API Key Not Configured**\n\n"
        "To use this app, add your RentCast API key:\n"
        "1. Sign up at [rentcast.io](https://rentcast.io)\n"
        "2. In Streamlit Cloud: Settings → Secrets → Add `RENTCAST_API_KEY`\n"
        "3. For local testing: Create `.streamlit/secrets.toml` with:\n"
        "   ```\n"
        "   RENTCAST_API_KEY = \"your-api-key-here\"\n"
        "   ```"
    )

if search_clicked and zip_input:
    # Parse ZIP codes
    zip_codes = [z.strip() for z in zip_input.split(",") if z.strip()]

    if not zip_codes:
        st.error("Please enter at least one ZIP code")
    elif not api_key:
        st.error("API key not configured. See instructions above.")
    else:
        # Validate ZIP codes
        valid_zips = []
        invalid_zips = []

        for zip_code in zip_codes:
            if len(zip_code) == 5 and zip_code.isdigit():
                if is_valid_zip(zip_code):
                    valid_zips.append(zip_code)
                else:
                    invalid_zips.append(zip_code)
            else:
                invalid_zips.append(zip_code)

        if invalid_zips:
            st.warning(f"ZIP codes not in HACC coverage area: {', '.join(invalid_zips)}")

        if valid_zips:
            # Show payment standards for searched ZIPs
            st.subheader("Payment Standards")
            cols = st.columns(min(len(valid_zips), 4))
            for i, zip_code in enumerate(valid_zips):
                payment_std = get_payment_standard(zip_code, bedrooms)
                with cols[i % 4]:
                    st.metric(
                        label=f"ZIP {zip_code}",
                        value=f"${payment_std:,}" if payment_std else "N/A"
                    )

            st.markdown("---")

            # Search each ZIP code
            all_listings = []
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, zip_code in enumerate(valid_zips):
                status_text.text(f"Searching {zip_code}...")
                progress_bar.progress((i + 1) / len(valid_zips))

                listings = search_rentals(zip_code, bedrooms, api_key)

                # Add ZIP code and payment standard to each listing
                payment_std = get_payment_standard(zip_code, bedrooms)
                for listing in listings:
                    listing["_search_zip"] = zip_code
                    listing["_payment_standard"] = payment_std

                all_listings.extend(listings)

            progress_bar.empty()
            status_text.empty()

            if not all_listings:
                st.info(f"No {bedroom_label.lower()} rentals found in the selected ZIP codes.")
            else:
                # Filter and sort listings
                qualifying = []
                over_budget = []

                for listing in all_listings:
                    price = listing.get("price")
                    payment_std = listing.get("_payment_standard")

                    if price is not None and payment_std is not None:
                        if price <= payment_std:
                            qualifying.append(listing)
                        else:
                            over_budget.append(listing)
                    else:
                        # Include listings without price in qualifying (may need manual check)
                        qualifying.append(listing)

                # Sort by price
                qualifying.sort(key=lambda x: x.get("price") or 0)
                over_budget.sort(key=lambda x: x.get("price") or 0)

                # Display results
                st.subheader(f"Qualifying Rentals ({len(qualifying)})")

                if qualifying:
                    for listing in qualifying:
                        address = listing.get("formattedAddress", "Address not available")
                        price = listing.get("price")
                        payment_std = listing.get("_payment_standard")
                        sqft = listing.get("squareFootage")
                        listing_id = listing.get("id", "")

                        with st.container():
                            col1, col2, col3 = st.columns([3, 1, 1])

                            with col1:
                                st.markdown(f"**{address}**")
                                details = []
                                if sqft:
                                    details.append(f"{sqft:,} sq ft")
                                if listing.get("propertyType"):
                                    details.append(listing.get("propertyType"))
                                if details:
                                    st.caption(" • ".join(details))

                            with col2:
                                st.markdown(f"**{format_price(price)}**")
                                if price and payment_std:
                                    savings = payment_std - price
                                    st.caption(f"${savings:,} under limit")

                            with col3:
                                if listing_id:
                                    st.link_button("View", f"https://rentcast.io/listing/{listing_id}")

                            st.markdown("---")
                else:
                    st.info("No qualifying rentals found within payment standards.")

                # Optionally show over-budget listings
                if over_budget:
                    with st.expander(f"Over Budget ({len(over_budget)})"):
                        st.caption("These rentals exceed the payment standard for their ZIP code.")
                        for listing in over_budget[:10]:  # Limit to first 10
                            address = listing.get("formattedAddress", "Address not available")
                            price = listing.get("price")
                            payment_std = listing.get("_payment_standard")

                            over_by = price - payment_std if price and payment_std else 0
                            st.markdown(
                                f"~~{address}~~ - {format_price(price)} "
                                f"(${over_by:,} over)"
                            )

elif search_clicked and not zip_input:
    st.error("Please enter at least one ZIP code")

# Footer
st.markdown("---")
st.caption(
    "Data from RentCast API. Payment standards from Housing Authority of Cook County (HACC), "
    "effective January 1, 2026. For HUD-VASH case managers."
)
