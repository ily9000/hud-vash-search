"""
HUD-VASH Rental Search Tool for Cook County, IL

A Streamlit web app that searches rental listings and filters by HACC payment standards.
"""

import streamlit as st
import requests
import json
import os
import urllib.parse
from payment_standards import (
    get_payment_standard,
    is_valid_zip,
    get_all_towns,
    resolve_location
)

# Page configuration
st.set_page_config(
    page_title="HUD-VASH Rental Search",
    page_icon="🏠",
    layout="wide"
)


def check_password():
    """Returns True if the user has entered the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets.get("APP_PASSWORD", ""):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.secrets.get("APP_PASSWORD"):
        if st.session_state.get("password_correct", False):
            return True

        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("Incorrect password")
        return False
    return True


if not check_password():
    st.stop()

# Veterans data file path
VETERANS_FILE = os.path.join(os.path.dirname(__file__), "veterans.json")


def load_veterans() -> dict:
    """Load veteran profiles from JSON file."""
    if os.path.exists(VETERANS_FILE):
        try:
            with open(VETERANS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_veterans(veterans: dict):
    """Save veteran profiles to JSON file."""
    with open(VETERANS_FILE, "w") as f:
        json.dump(veterans, f, indent=2)


def get_api_key():
    """Get RentCast API key from Streamlit secrets."""
    try:
        return st.secrets["RENTCAST_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def search_rentals(zip_code: str, api_key: str, bedrooms: int | None = None) -> list[dict]:
    """Search RentCast API for rental listings.

    If bedrooms is None, returns all listings regardless of bedroom count.
    """
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

    # Only filter by bedrooms if specified
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


def is_not_interested(listing: dict, not_interested_list: list) -> bool:
    """Check if a listing is in the not_interested list (by address + price)."""
    address = listing.get("formattedAddress", "")
    price = listing.get("price")
    for item in not_interested_list:
        if item.get("address") == address and item.get("price") == price:
            return True
    return False


def add_not_interested(veteran_name: str, address: str, price: int | float | None, veterans: dict):
    """Add a listing to a veteran's not_interested list."""
    if veteran_name not in veterans:
        return
    if "not_interested" not in veterans[veteran_name]:
        veterans[veteran_name]["not_interested"] = []
    # Check if already in list
    for item in veterans[veteran_name]["not_interested"]:
        if item.get("address") == address and item.get("price") == price:
            return  # Already exists
    veterans[veteran_name]["not_interested"].append({"address": address, "price": price})
    save_veterans(veterans)


def remove_not_interested(veteran_name: str, address: str, price: int | float | None, veterans: dict):
    """Remove a listing from a veteran's not_interested list."""
    if veteran_name not in veterans:
        return
    if "not_interested" not in veterans[veteran_name]:
        return
    veterans[veteran_name]["not_interested"] = [
        item for item in veterans[veteran_name]["not_interested"]
        if not (item.get("address") == address and item.get("price") == price)
    ]
    save_veterans(veterans)


# Title
st.title("HUD-VASH Rental Search")
st.markdown("**Cook County, IL** - Search rentals within HACC payment standards")
st.markdown("---")

# Load veterans data
veterans = load_veterans()

# Sidebar with search form
with st.sidebar:
    st.header("Search")

    # Veteran selector
    veteran_options = ["-- New Search --"] + sorted(veterans.keys())
    selected_veteran = st.selectbox("Select Veteran", options=veteran_options)

    # Get defaults from selected veteran
    if selected_veteran != "-- New Search --" and selected_veteran in veterans:
        default_towns = ", ".join(veterans[selected_veteran].get("towns", []))
        default_bedrooms = veterans[selected_veteran].get("bedrooms", 1)
    else:
        default_towns = ""
        default_bedrooms = 1

    # Bedroom options mapping
    bedroom_options = {
        "Studio": 0,
        "1 Bedroom": 1,
        "2 Bedroom": 2,
        "3 Bedroom": 3,
        "4 Bedroom": 4
    }
    bedroom_labels = list(bedroom_options.keys())
    default_bedroom_index = list(bedroom_options.values()).index(default_bedrooms) if default_bedrooms in bedroom_options.values() else 1

    # Voucher bedroom size (what the veteran is entitled to)
    voucher_label = st.selectbox(
        "Voucher Bedroom Size",
        options=bedroom_labels,
        index=default_bedroom_index,
        help="The veteran's voucher entitlement (used for payment standard calculation)"
    )
    voucher_bedrooms = bedroom_options[voucher_label]

    # Bedroom search filter (which unit sizes to show)
    default_search_filter = [voucher_label]  # Default to voucher size
    search_bedroom_labels = st.multiselect(
        "Search for Bedrooms",
        options=bedroom_labels,
        default=default_search_filter,
        help="Which unit sizes to search for (can select multiple)"
    )
    # Convert labels to bedroom counts
    search_bedrooms = [bedroom_options[label] for label in search_bedroom_labels]

    # Town selector with autocomplete (multiselect with search)
    all_towns = get_all_towns()

    # Parse default towns into list for multiselect
    default_town_list = [t.strip() for t in default_towns.split(",") if t.strip() and t.strip() in all_towns]

    selected_towns = st.multiselect(
        "Select Towns",
        options=all_towns,
        default=default_town_list,
        placeholder="Type to search towns...",
        help="Start typing to filter towns, then click to select"
    )

    # Additional ZIP codes input (optional)
    extra_zips = st.text_input(
        "Additional ZIP Codes (optional)",
        placeholder="60601, 60602",
        help="Add specific ZIP codes not covered by town selection"
    )

    # Combine selected towns and extra zips for the search
    location_input = ", ".join(selected_towns)
    if extra_zips:
        location_input = f"{location_input}, {extra_zips}" if location_input else extra_zips

    # Search button
    search_clicked = st.button("Search", type="primary", use_container_width=True)

    st.markdown("---")

    # Add/Edit Veteran section
    with st.expander("Manage Veterans"):
        # Edit existing veteran
        if veterans:
            st.subheader("Edit Veteran")
            edit_veteran = st.selectbox(
                "Select veteran to edit",
                options=[""] + sorted(veterans.keys()),
                key="edit_vet_select"
            )

            if edit_veteran:
                vet_data = veterans[edit_veteran]
                current_towns = vet_data.get("towns", [])
                current_br = vet_data.get("bedrooms", 1)
                current_br_index = list(bedroom_options.values()).index(current_br) if current_br in bedroom_options.values() else 1

                edit_towns = st.multiselect(
                    "Preferred Towns",
                    options=all_towns,
                    default=current_towns,
                    key="edit_vet_towns",
                    placeholder="Type to search..."
                )
                edit_br = st.selectbox(
                    "Voucher Bedroom Size",
                    options=bedroom_labels,
                    index=current_br_index,
                    key="edit_vet_br"
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save Changes", key="save_edit"):
                        veterans[edit_veteran] = {
                            "towns": edit_towns,
                            "bedrooms": bedroom_options[edit_br]
                        }
                        save_veterans(veterans)
                        st.success(f"Updated {edit_veteran}")
                        st.rerun()
                with col2:
                    if st.button("Delete", type="secondary", key="delete_edit"):
                        del veterans[edit_veteran]
                        save_veterans(veterans)
                        st.success(f"Deleted {edit_veteran}")
                        st.rerun()

            st.markdown("---")

        # Add new veteran
        st.subheader("Add New Veteran")
        new_veteran_name = st.text_input("Veteran Name", key="new_vet_name")
        new_veteran_towns = st.multiselect(
            "Preferred Towns",
            options=all_towns,
            key="new_vet_towns",
            placeholder="Type to search..."
        )
        new_veteran_bedrooms = st.selectbox(
            "Voucher Bedroom Size",
            options=bedroom_labels,
            key="new_vet_bedrooms"
        )

        if st.button("Add Veteran"):
            if new_veteran_name:
                if new_veteran_name in veterans:
                    st.error(f"{new_veteran_name} already exists. Select them above to edit.")
                else:
                    veterans[new_veteran_name] = {
                        "towns": new_veteran_towns,
                        "bedrooms": bedroom_options[new_veteran_bedrooms]
                    }
                    save_veterans(veterans)
                    st.success(f"Added {new_veteran_name}")
                    st.rerun()
            else:
                st.error("Please enter a veteran name")

    st.markdown("---")
    st.markdown("**Payment Standards:** HACC 2026")
    st.caption(f"Available towns: {len(get_all_towns())}")


# Main content area - Search Results
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
    # Parse locations (towns or ZIP codes)
    locations = [loc.strip() for loc in location_input.split(",") if loc.strip()]

    if not locations:
        st.error("Please enter at least one town or ZIP code")
    elif not api_key:
        st.error("API key not configured. See instructions above.")
    else:
        # Resolve all locations to ZIP codes
        all_zips = []
        unresolved = []

        for loc in locations:
            zips = resolve_location(loc)
            if zips:
                all_zips.extend(zips)
            else:
                unresolved.append(loc)

        # Remove duplicates while preserving order
        valid_zips = list(dict.fromkeys(all_zips))

        if unresolved:
            st.warning(f"Could not find: {', '.join(unresolved)}")

        if valid_zips:
            # Show what we're searching
            st.info(f"Searching {len(valid_zips)} ZIP codes: {', '.join(valid_zips[:10])}{'...' if len(valid_zips) > 10 else ''}")

            # Show payment standards for searched ZIPs (based on voucher bedroom size)
            st.subheader(f"Payment Standards ({voucher_label} Voucher)")
            display_zips = valid_zips[:8]  # Show max 8
            cols = st.columns(min(len(display_zips), 4))
            for i, zip_code in enumerate(display_zips):
                payment_std = get_payment_standard(zip_code, voucher_bedrooms)
                with cols[i % 4]:
                    st.metric(
                        label=f"ZIP {zip_code}",
                        value=f"${payment_std:,}" if payment_std else "N/A"
                    )

            st.markdown("---")

            # Search each ZIP code - get ALL listings (not filtered by bedroom)
            all_listings = []
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, zip_code in enumerate(valid_zips):
                status_text.text(f"Searching {zip_code}...")
                progress_bar.progress((i + 1) / len(valid_zips))

                # Search without bedroom filter to get all listings
                listings = search_rentals(zip_code, api_key)

                # Add ZIP code to each listing
                # Payment standard rule:
                # - If unit is smaller than voucher size: use unit's bedroom standard
                # - If unit is larger than voucher size: use voucher's bedroom standard (capped)
                for listing in listings:
                    listing["_search_zip"] = zip_code
                    listing_bedrooms = listing.get("bedrooms", 0) or 0
                    # Use the lesser of unit bedrooms or voucher bedrooms
                    effective_bedrooms = min(listing_bedrooms, voucher_bedrooms)
                    listing["_payment_standard"] = get_payment_standard(zip_code, effective_bedrooms)

                all_listings.extend(listings)

            progress_bar.empty()
            status_text.empty()

            if not all_listings:
                st.info(f"No rentals found in the selected areas.")
            else:
                # Filter by selected bedroom sizes
                if search_bedrooms:
                    all_listings = [
                        listing for listing in all_listings
                        if (listing.get("bedrooms", 0) or 0) in search_bedrooms
                    ]

                # Get not_interested list for selected veteran
                not_interested_list = []
                if selected_veteran != "-- New Search --" and selected_veteran in veterans:
                    not_interested_list = veterans[selected_veteran].get("not_interested", [])

                # Filter to only show affordable listings (within payment standard)
                affordable_listings = []
                not_interested_listings = []
                for listing in all_listings:
                    price = listing.get("price")
                    payment_std = listing.get("_payment_standard")

                    # Check if within payment standard
                    is_affordable = (price is None or payment_std is None or payment_std == 0 or price <= payment_std)

                    if is_affordable:
                        # Check if in not_interested list
                        if is_not_interested(listing, not_interested_list):
                            not_interested_listings.append(listing)
                        else:
                            affordable_listings.append(listing)

                # Sort by price
                affordable_listings.sort(key=lambda x: x.get("price") or 0)
                not_interested_listings.sort(key=lambda x: x.get("price") or 0)

                # Display summary
                st.success(f"Found {len(affordable_listings)} affordable listings within payment standard.")

                # Display affordable listings
                st.subheader(f"Affordable Listings ({len(affordable_listings)})")

                if affordable_listings:
                    for i, listing in enumerate(affordable_listings):
                        address = listing.get("formattedAddress", "Address not available")
                        price = listing.get("price")
                        payment_std = listing.get("_payment_standard")
                        sqft = listing.get("squareFootage")
                        listing_br = listing.get("bedrooms", 0) or 0

                        # Bedroom label
                        br_display = "Studio" if listing_br == 0 else f"{listing_br} BR"

                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 0.5])

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
                                    st.caption(f"${savings:,} under limit")

                            with col3:
                                # Build search-friendly address formats
                                zillow_addr = address.replace(",", "").replace(" ", "-")
                                zillow_url = f"https://www.zillow.com/homes/{zillow_addr}_rb/"
                                apartments_query = urllib.parse.quote(address)
                                apartments_url = f"https://www.apartments.com/{apartments_query}/"
                                google_query = urllib.parse.quote(f"{address} for rent")
                                google_url = f"https://www.google.com/search?q={google_query}"

                                st.markdown(f"[Zillow]({zillow_url})")
                                st.markdown(f"[Apartments.com]({apartments_url})")
                                st.markdown(f"[Google]({google_url})")

                            # Not Interested button hidden for now
                            # with col4:
                            #     if selected_veteran != "-- New Search --":
                            #         if st.button("X", key=f"not_int_{i}", help="Not interested"):
                            #             add_not_interested(selected_veteran, address, price, veterans)
                            #             st.rerun()

                            st.markdown("---")
                else:
                    st.info("No affordable listings found matching your criteria.")

                # Not Interested section hidden for now
                # if not_interested_listings and selected_veteran != "-- New Search --":
                #     with st.expander(f"Not Interested ({len(not_interested_listings)})"):
                #         st.caption("Listings this veteran marked as not interested. Click Restore to show again.")
                #         for i, listing in enumerate(not_interested_listings):
                #             address = listing.get("formattedAddress", "Address not available")
                #             price = listing.get("price")
                #             listing_br = listing.get("bedrooms", 0) or 0
                #             br_display = "Studio" if listing_br == 0 else f"{listing_br}BR"
                #
                #             col1, col2 = st.columns([4, 1])
                #             with col1:
                #                 st.markdown(f"**{br_display}** - {address} - **{format_price(price)}**")
                #             with col2:
                #                 if st.button("Restore", key=f"restore_{i}"):
                #                     remove_not_interested(selected_veteran, address, price, veterans)
                #                     st.rerun()
        else:
            st.error("No valid locations found. Try entering town names like 'Evanston' or ZIP codes like '60601'.")

elif search_clicked and not location_input:
    st.error("Please enter at least one town or ZIP code")

# Footer
st.markdown("---")
st.caption(
    "Data from RentCast API. Payment standards from Housing Authority of Cook County (HACC), "
    "effective January 1, 2026. For HUD-VASH case managers."
)
