# HUD-VASH Rental Search Tool

A web app for VA HUD-VASH case managers to search rental listings within HACC payment standards for Cook County, IL.

## Features

- Search by bedroom count (Studio through 4BR)
- Enter multiple ZIP codes at once
- Automatically filters listings by HACC payment standards
- Shows qualifying rentals with price comparison

## Setup Instructions

### 1. Get a RentCast API Key

1. Go to [rentcast.io](https://rentcast.io)
2. Sign up for a free account
3. Navigate to API settings and copy your API key
4. Free tier includes 50 API calls/month

### 2. Deploy to Streamlit Cloud (Recommended)

1. **Create a GitHub account** (if you don't have one): [github.com](https://github.com)

2. **Upload this code to GitHub**:
   - Click "New repository"
   - Name it `hud-vash-search`
   - Upload all files from this folder

3. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your `hud-vash-search` repository
   - Set main file path to `app.py`
   - Click "Deploy"

4. **Add your API key**:
   - In your deployed app, click "Settings" (gear icon)
   - Go to "Secrets"
   - Add:
     ```
     RENTCAST_API_KEY = "your-api-key-here"
     ```
   - Click "Save"

5. **Share the app URL** with your team

### 3. Run Locally (Optional)

For testing before deployment:

```bash
# Install dependencies
pip install -r requirements.txt

# Create secrets file
mkdir -p .streamlit
echo 'RENTCAST_API_KEY = "your-api-key-here"' > .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

The app will open at http://localhost:8501

## Usage

1. Select bedroom count from the dropdown
2. Enter one or more ZIP codes (comma-separated)
3. Click "Search"
4. Review qualifying rentals that fall within payment standards

## Payment Standards

This app uses HACC (Housing Authority of Cook County) payment standards effective January 1, 2026. To update the standards when new rates are published, the `payment_standards.py` file needs to be updated.

## Files

- `app.py` - Main Streamlit application
- `payment_standards.py` - HACC payment standards lookup table
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Support

For issues with this tool, contact your IT support or the developer who set it up.
