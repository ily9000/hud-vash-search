#!/usr/bin/env python3
"""Test script to inspect RentCast API response structure."""

import requests
import json
import sys
import os

def test_rentcast_api(api_key: str, zip_code: str = "60601"):
    """Make a test call and print full response structure."""
    url = "https://api.rentcast.io/v1/listings/rental/long-term"

    headers = {
        "Accept": "application/json",
        "X-Api-Key": api_key
    }

    params = {
        "zipCode": zip_code,
        "status": "Active",
        "limit": 1  # Just get 1 listing to see structure
    }

    print(f"Fetching rental listing from ZIP {zip_code}...")
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not data:
        print("No listings found in this ZIP code.")
        return

    # Get first listing
    listing = data[0] if isinstance(data, list) else data

    print("\n" + "="*60)
    print("FULL RESPONSE STRUCTURE (first listing)")
    print("="*60)
    print(json.dumps(listing, indent=2))

    print("\n" + "="*60)
    print("ALL KEYS IN RESPONSE")
    print("="*60)
    for key in sorted(listing.keys()):
        value = listing[key]
        value_type = type(value).__name__
        preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
        print(f"  {key}: ({value_type}) {preview}")

    # Check for photo-related fields
    print("\n" + "="*60)
    print("PHOTO-RELATED FIELDS")
    print("="*60)
    photo_keywords = ['photo', 'image', 'img', 'media', 'picture', 'thumbnail', 'url']
    found_photo_fields = []

    for key in listing.keys():
        key_lower = key.lower()
        if any(kw in key_lower for kw in photo_keywords):
            found_photo_fields.append(key)
            print(f"  Found: {key} = {listing[key]}")

    if not found_photo_fields:
        print("  No photo-related fields found in response.")

if __name__ == "__main__":
    # Try environment variable first
    api_key = os.environ.get("RENTCAST_API_KEY")

    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]

    if not api_key:
        print("Usage: python test_rentcast_response.py YOUR_API_KEY [ZIP_CODE]")
        print("   or: RENTCAST_API_KEY=xxx python test_rentcast_response.py [ZIP_CODE]")
        sys.exit(1)

    zip_code = sys.argv[2] if len(sys.argv) > 2 else "60601"

    try:
        test_rentcast_api(api_key, zip_code)
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        sys.exit(1)
