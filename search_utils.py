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

    # Custom CSS for this page
    st.markdown("""
    <style>
        /* Listing card styling */
        .listing-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            transition: box-shadow 0.2s;
        }
        .listing-card:hover {
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        /* Affordable badge */
        .affordable-badge {
            background: #d4edda;
            color: #155724;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        /* Price highlight */
        .price-highlight {
            font-size: 1.25rem;
            font-weight: bold;
            color: #1e3a5f;
        }

        /* Savings badge */
        .savings-badge {
            background: #e8f5e9;
            color: #2e7d32;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        /* Info callout */
        .info-callout {
            background: #e3f2fd;
            border-left: 4px solid #1976d2;
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            margin: 1rem 0;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: #f8f9fa;
        }
    </style>
    """, unsafe_allow_html=True)

    # Page title with context
    st.title(f"🏠 {county['name']} Rental Search")
    st.markdown(f"Finding affordable rentals within **{county['authority']}** payment standards")

    # Quick help for new users
    st.markdown("""
    <div class="info-callout">
        <strong>💡 Quick Guide:</strong> Use the sidebar on the left to set your search criteria,
        then click "Search Rentals" to find listings your client can afford.
    </div>
    """, unsafe_allow_html=True)

    # Show payment standards explainer in an expander
    with st.expander("📋 How Payment Standards Work in This County", expanded=False):
        st.markdown(county['explainer'])
        st.caption(f"Payment standards effective: {county['effective_date']}")

    st.markdown("---")

    # Sidebar with search form
    with st.sidebar:
        st.markdown("## 🔍 Search Settings")
        st.caption("Set up your search criteria below")

        st.markdown("---")

        # Bedroom options with clearer labeling
        bedroom_options = {
            "Studio": 0,
            "1 Bedroom": 1,
            "2 Bedroom": 2,
            "3 Bedroom": 3,
            "4 Bedroom": 4
        }
        bedroom_labels = list(bedroom_options.keys())

        st.markdown("**🎫 Client's Voucher Size**")
        voucher_label = st.selectbox(
            "Voucher Bedroom Size",
            options=bedroom_labels,
            index=1,
            help="This is on the voucher paperwork. It determines the maximum rent HUD will cover.",
            label_visibility="collapsed"
        )
        voucher_bedrooms = bedroom_options[voucher_label]
        st.caption(f"Selected: {voucher_label} voucher")

        st.markdown("")
        st.markdown("**🛏️ Unit Sizes to Search**")
        search_bedroom_labels = st.multiselect(
            "Unit Sizes to Search",
            options=bedroom_labels,
            default=[voucher_label],
            help="Tip: You can search for larger units than the voucher size, but the voucher limit still applies.",
            label_visibility="collapsed"
        )
        search_bedrooms = [bedroom_options[label] for label in search_bedroom_labels]

        st.markdown("---")

        # Town selector with better guidance
        all_towns = get_all_towns(county_key)

        st.markdown("**📍 Where to Search**")
        selected_towns = st.multiselect(
            "Select Towns",
            options=all_towns,
            placeholder="Start typing a town name...",
            help="Select one or more towns. Each town may cover multiple ZIP codes.",
            label_visibility="collapsed"
        )

        # Resolve and display ZIP codes for selected towns
        resolved_zips = []
        if selected_towns:
            for town in selected_towns:
                town_zips = resolve_location(county_key, town)
                if town_zips:
                    resolved_zips.extend(town_zips)
            resolved_zips = list(dict.fromkeys(resolved_zips))  # Remove duplicates

        # Pre-fill ZIP codes field with resolved ZIPs
        default_zips = ", ".join(resolved_zips) if resolved_zips else ""

        extra_zips = st.text_input(
            "ZIP Codes",
            value=default_zips,
            placeholder="60601, 60602",
            help="Auto-filled from town selection. You can add or remove ZIP codes.",
            label_visibility="visible"
        )

        location_input = extra_zips  # Now just use the ZIP codes directly

        st.markdown("")
        search_clicked = st.button("🔍 Search Rentals", type="primary", use_container_width=True)

        if not location_input:
            st.caption("⚠️ Select at least one town or enter a ZIP code")

        st.markdown("---")

        # County info footer
        st.markdown("**📋 Current County**")
        st.markdown(f"{county['name']}")
        st.caption(f"🏛️ {county['authority']}")
        st.caption(f"📅 Standards effective: {county['effective_date']}")
        st.caption(f"📍 {len(all_towns)} towns available")

        # Link back to home
        st.markdown("---")
        st.page_link("app.py", label="← Change County", icon="🔄")

    # Main content
    api_key = get_api_key()

    if not api_key:
        st.warning(
            "**⚙️ Setup Required: API Key Not Configured**\n\n"
            "To use this app, you need a RentCast API key:\n"
            "1. Sign up at [rentcast.io](https://rentcast.io)\n"
            "2. In Streamlit Cloud: Settings → Secrets → Add `RENTCAST_API_KEY`\n"
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
                st.info(f"🔎 Searching **{len(valid_zips)}** ZIP codes: {', '.join(valid_zips[:10])}{'...' if len(valid_zips) > 10 else ''}")

                # Show payment standards with better explanation
                st.markdown(f"### 💰 Payment Limits for {voucher_label} Voucher")
                st.caption("These are the maximum rents HUD will cover in each ZIP code. Listings above these amounts will be filtered out.")

                display_zips = valid_zips[:8]
                cols = st.columns(min(len(display_zips), 4))
                for i, zip_code in enumerate(display_zips):
                    payment_std = get_payment_standard(county_key, zip_code, voucher_bedrooms)
                    with cols[i % 4]:
                        st.metric(
                            label=f"ZIP {zip_code}",
                            value=f"${payment_std:,}/mo" if payment_std else "N/A"
                        )

                if len(valid_zips) > 8:
                    st.caption(f"*Showing 8 of {len(valid_zips)} ZIP codes*")

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
                    st.info("📭 No rentals currently listed in the selected areas. Try expanding your search to nearby towns.")
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

                    # Success message with context
                    if len(affordable_listings) > 0:
                        st.success(f"✅ Found **{len(affordable_listings)}** affordable listings within your client's payment standard!")
                    else:
                        st.warning("No affordable listings found in the selected areas.")

                    st.markdown(f"### 🏠 Affordable Listings ({len(affordable_listings)})")
                    st.caption("Sorted by price (lowest first). All listings below are within the payment standard.")

                    if affordable_listings:
                        for listing in affordable_listings:
                            address = listing.get("formattedAddress", "Address not available")
                            price = listing.get("price")
                            payment_std = listing.get("_payment_standard")
                            sqft = listing.get("squareFootage")
                            listing_br = listing.get("bedrooms", 0) or 0

                            br_display = "Studio" if listing_br == 0 else f"{listing_br} Bedroom"

                            with st.container(border=True):
                                col1, col2, col3 = st.columns([3, 1.5, 1.2])

                                with col1:
                                    st.markdown(f"**📍 {address}**")
                                    # Build details with icons
                                    details = [f"🛏️ {br_display}"]
                                    if sqft:
                                        details.append(f"📐 {sqft:,} sq ft")
                                    if listing.get("propertyType"):
                                        prop_type = listing.get("propertyType", "").replace("_", " ").title()
                                        details.append(f"🏢 {prop_type}")
                                    st.caption(" • ".join(details))

                                with col2:
                                    st.markdown(f"### {format_price(price)}")
                                    if price and payment_std:
                                        savings = payment_std - price
                                        if savings > 0:
                                            st.markdown(f"✅ **${savings:,}** under limit")
                                        elif savings == 0:
                                            st.caption("At limit")

                                with col3:
                                    google_query = urllib.parse.quote(f"{address} rental")
                                    google_url = f"https://www.google.com/search?q={google_query}"
                                    st.link_button("🔗 View on Google", google_url, use_container_width=True)

                    else:
                        st.markdown("""
                        **No listings found matching your criteria.**

                        Try these tips:
                        - Expand your search to more towns or ZIP codes
                        - Search for different bedroom sizes
                        - Check back later (new listings are added daily)
                        """)
            else:
                st.error(f"❌ No valid locations found in {county['name']}. Please check your town names or ZIP codes.")

    elif search_clicked and not location_input:
        st.error("⚠️ Please select at least one town or enter a ZIP code in the sidebar")

    elif not search_clicked and api_key:
        # Welcome state with helpful guidance
        st.markdown("""
        ### 👋 Ready to Search!

        Use the **sidebar on the left** to set up your search:

        1. **Set the voucher size** - Match your client's voucher paperwork
        2. **Choose unit sizes** - What size units are you looking for?
        3. **Pick locations** - Select towns or enter ZIP codes
        4. **Click Search** - Find affordable listings instantly

        All results will be filtered to show only rentals within your client's payment standard.
        """)

    # Footer with helpful context
    st.markdown("---")
    col_foot1, col_foot2 = st.columns(2)
    with col_foot1:
        st.caption(
            f"📊 Data from RentCast API • Payment standards from {county['authority']} "
            f"(effective {county['effective_date']})"
        )
    with col_foot2:
        st.caption(
            "💡 **Tip:** Always call landlords to verify availability and confirm they accept HUD-VASH vouchers."
        )
