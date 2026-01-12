# HUD-VASH Rental Search Tool

A web app that helps VA case managers find affordable housing for homeless veterans. Currently configured for Cook County, IL, with plans to expand nationwide.

## The Problem

HUD-VASH case managers help homeless veterans find housing using housing vouchers. Finding a qualifying rental is tedious and time-consuming:

- **Payment standards vary by ZIP code** - every housing authority sets different rates by location. For example, Cook County alone has 26 different payment tiers across 130+ towns
- **The "lesser of" rule is confusing** - if a veteran with a 2BR voucher wants a 3BR unit, the payment standard is capped at the 2BR rate
- **Manual searching takes time** - about 20 minutes per veteran per week checking Zillow, Apartments.com, and Craigslist, then cross-referencing against payment standard tables. Across hundreds of veterans nationwide, this adds up fast
- **No way to track progress** - which listings has this veteran already seen and rejected?

## What This Tool Does

- **Searches rental listings** by town or ZIP code
- **Automatically applies payment standards** using HACC 2026 rates
- **Handles the "lesser of" rule** correctly
- **Saves veteran profiles** with preferred towns and voucher size
- **Tracks "Not Interested" listings** so rejected properties don't keep showing up
- **Links directly to Zillow, Apartments.com, and Google** for each listing

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

1. **Select a veteran** from the dropdown (or "New Search" for quick lookups)
2. **Set voucher size** - their bedroom entitlement
3. **Pick bedroom sizes to search** - can select multiple
4. **Select towns** - type to search, click to add
5. **Click Search**

Results show only listings within the payment standard. Click **X** to mark listings as "Not Interested" for that veteran.

## Data

- **Listings**: RentCast API
- **Payment Standards**: Housing Authority of Cook County (HACC), effective January 1, 2026
