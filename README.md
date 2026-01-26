# HUD-VASH Rental Search Tool

A web app that helps HUD-VASH case managers find affordable housing for homeless veterans in Illinois. Supports Cook, DuPage, Will, and Lake counties.

## The Problem

HUD-VASH case managers help homeless veterans find housing using housing vouchers. Finding a qualifying rental is tedious and time-consuming:

- **Payment standards vary by ZIP code** - every housing authority sets different rates by location
- **The "lesser of" rule is confusing** - if a veteran with a 2BR voucher wants a 3BR unit, the payment standard is capped at the 2BR rate
- **Manual searching takes time** - checking Zillow, Apartments.com, and Craigslist, then cross-referencing against payment standard tables

## What This Tool Does

- **Searches rental listings** by town or ZIP code using RentCast API
- **Automatically applies payment standards** for each county's housing authority
- **Handles the "lesser of" rule** correctly
- **Shows payment standards in real-time** as you select locations
- **Links to official payment standard documents** for verification

## Supported Counties

| County | Housing Authority | Effective Date |
|--------|------------------|----------------|
| Cook | Housing Authority of Cook County (HACC) | January 1, 2026 |
| DuPage | DuPage Housing Authority (DHA) | January 1, 2025 |
| Will | Housing Authority of Joliet (HAJ) | October 1, 2025 |
| Lake | Lake County Housing Authority (LCHA) | January 1, 2026 |

## How Payment Standards Work

The app uses the "lesser of" rule - the payment standard is based on whichever is smaller: the unit's bedroom count or the voucher's bedroom count.

**Example**: A veteran has a 2BR voucher.

| Unit They Find | Payment Standard Used | Why |
|----------------|----------------------|-----|
| 1BR | 1BR rate | Unit is smaller than voucher |
| 2BR | 2BR rate | Exact match |
| 3BR | 2BR rate | Capped at voucher size |

This means veterans can look at larger units, but HUD won't pay more than their voucher allows.

## Quick Start

1. **Select a county** from the home page
2. **Set voucher size** - the client's bedroom entitlement
3. **Pick bedroom sizes to search** - can select multiple
4. **Select towns** or enter ZIP codes directly
5. **Review payment standards** shown in the sidebar
6. **Click Search** to find affordable listings

Results show only listings within the payment standard.

## Data Sources

- **Listings**: [RentCast API](https://rentcast.io)
- **Payment Standards**: Official documents from each housing authority (linked in app)

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your RentCast API key to `.streamlit/secrets.toml`:
   ```toml
   RENTCAST_API_KEY = "your-api-key-here"
   ```
4. Run: `streamlit run app.py`

## Payment Standards Sources

Each county's payment standards are sourced from official housing authority documents:

- **Cook County**: [HACC Payment Standards PDF](https://thehacc.org/app/uploads/2025/11/Payment-Standard-Eff-1-2026.pdf)
- **DuPage County**: [DHA Payment Standards](https://www.dupagehousing.org/dupage-payment-standards)
- **Will County**: [HAJ Payment Standards PDF](https://www.hajoliet.org/sites/default/files/file-attachements/2026_haj_payment_standards.10-2025.pdf)
- **Lake County**: [LCHA Payment Standards](https://www.lakecountyha.org/plugins/show_image.php?id=1662)
