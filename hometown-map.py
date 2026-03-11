import pandas as pd
import requests
import folium
import os
from dotenv import load_dotenv
import time

# ============================================================
# STEP 1 — LOAD MAPBOX TOKEN FROM .env (keeps it off GitHub)
# ============================================================
load_dotenv()
ACCESS_TOKEN = os.getenv("MAPBOX_TOKEN")

if not ACCESS_TOKEN:
    raise ValueError("MAPBOX_TOKEN not found. Did you create a .env file?")

# Your custom Mapbox style URL (uses token from .env)
MAPBOX_TILES = (
    f"https://api.mapbox.com/styles/v1/mgordy/cmmk2hq74002p01s17m3cg2iw/"
    f"tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={ACCESS_TOKEN}"
)

# ============================================================
# STEP 2 — GEOCODING FUNCTION
# ============================================================

def geocode_address(address_string, ACCESS_TOKEN):
    """
    Look up the lat/lon coordinates for a text address using Mapbox.

    Parameters:
        address_string (str): The full address to look up, e.g.,
                              "1160 Oak Knoll Ave, Napa, California 94558"
        token (str): Your Mapbox public access token

    Returns:
        tuple: (latitude, longitude) as floats, or (None, None) if lookup fails
    """
    
    # Convert to string and handle NaN values from pandas
    address_string = str(address_string) if address_string is not None else ""
    
    # Skip addresses that are blank, NaN, or PO Boxes — Mapbox can't place those
    # on a map because they don't represent a physical street location.
    if not address_string or address_string == "nan" or "P.O. Box" in address_string or "PO Box" in address_string:
        return None, None

    # Build the Mapbox Geocoding API URL.
    # The Mapbox v6 "forward geocoding" endpoint converts text → coordinates.
    # We include the token for authentication.
    # "country=us" limits results to the United States (improves accuracy)
    # "limit=1" means only return the single most relevant result
    geocode_url = (
        f"https://api.mapbox.com/search/geocode/v6/forward"
        f"?q={requests.utils.quote(address_string)}"  # URL-encode the address
        f"&country=us"
        f"&limit=1"
        f"&access_token={ACCESS_TOKEN}"
    )

    try:
        # Send the request and wait up to 10 seconds for a response
        response = requests.get(geocode_url, timeout=10)

        # Check if the request was successful
        if response.status_code != 200:
            return None, None

        # Parse the JSON response into a Python dictionary
        data = response.json()

        # Navigate the JSON structure to get the coordinates.
        # Mapbox returns results in a 'features' list. The first item
        # is the best match. Coordinates are stored as [longitude, latitude].
        features = data.get("features", [])
        if features:
            coords = features[0]["geometry"]["coordinates"]
            longitude = coords[0]
            latitude = coords[1]
            return latitude, longitude

    except requests.exceptions.RequestException:
        # If anything goes wrong with the request, return None
        return None, None

    return None, None  # Fallback if no features were found

# ============================================================
# STEP 3 — LOAD YOUR HOMETOWN CSV
# ============================================================
CSV_FILE = "hometown_locations.csv"   # update if needed
df = pd.read_csv(CSV_FILE)

print(f"Loaded {len(df)} locations from {CSV_FILE}")

df["lat"] = None
df["lon"] = None

# ============================================================
# STEP 4 — GEOCODE EACH LOCATION
# ============================================================
print("\nGeocoding addresses using Mapbox API...")
print("(This may take a minute — we pause briefly between each request\n"
      " to avoid overwhelming the API server.)")

# Create empty lists to store the coordinates we get back
latitudes = []
longitudes = []

# Loop through each row in the DataFrame using iterrows().
# 'i' is the row index (0, 1, 2...), 'row' is the row data.
for count, (i, row) in enumerate(df.iterrows(), start=1):

    # Build the full address string for geocoding.
    # We combine the address fields for the best possible result.
    address = row.get("Address", "")

    # Show progress so students can see the script is working
    name = str(row.get("Name", f"Row {count}"))
    print(f"[{count}/{len(df)}] Geocoding: {name[:40]}...")

    # Call our geocoding function
    lat, lon = geocode_address(address, ACCESS_TOKEN)

    # Append the result to our lists
    latitudes.append(lat)
    longitudes.append(lon)

    # time.sleep() pauses execution for 0.1 seconds between requests.
    # This is called "rate limiting" — it's considerate to API servers
    # and prevents your account from being flagged for excessive requests.
    time.sleep(0.1)

# Add the latitude and longitude as new columns in our DataFrame
df["Latitude"] = latitudes
df["Longitude"] = longitudes

# Count how many addresses were successfully geocoded
geocoded_count = df["Latitude"].notna().sum()
print(f"\nSuccessfully geocoded: {geocoded_count} out of {len(df)} locations")
print(f"Could not geocode:      {len(df) - geocoded_count} locations")
print("  (PO Boxes, missing addresses, and very rural locations may not geocode)")

# ============================================================
# STEP 5 — CREATE FOLIUM MAP WITH CUSTOM MAPBOX STYLE
# ============================================================
valid = df.dropna(subset=["Latitude", "Longitude"])

if valid.empty:
    raise ValueError("No valid coordinates found. Check your addresses.")

center_lat = valid["Latitude"].mean()
center_lon = valid["Longitude"].mean()

hometown_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles=MAPBOX_TILES,
    attr="Mapbox"
)

# Color mapping for location types
COLOR_MAP = {
    "restaurant": "red",
    "park": "green",
    "cultural": "purple",
    "museum": "blue",
    "default": "gray"
}

title_html = """
<div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
     z-index: 1000; background-color: rgba(255,255,255,0.9); padding: 10px 20px;
     border: 2px solid #8B0000; border-radius: 8px; font-family: Georgia, serif;
     font-size: 16px; font-weight: bold; color: #8B0000; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
    🏡 Hometown Map of Frederick, MD
</div>
"""
hometown_map.get_root().html.add_child(folium.Element(title_html))


# ============================================================
# STEP 6 — ADD MARKERS WITH POPUPS
# ============================================================
for _, row in valid.iterrows():
    loc_type = str(row["Type"]).lower()
    color = COLOR_MAP.get(loc_type, COLOR_MAP["default"])

    popup_html = f"""
    <h4>{row['Name']}</h4>
    <p>{row['Description']}</p>
    <img src="{row['Image_URL']}" width="200px">
    """

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(hometown_map)

# ============================================================
# STEP 7 — SAVE MAP
# ============================================================
OUTPUT_HTML = "hometown_map.html"
hometown_map.save(OUTPUT_HTML)

print(f"\nMap saved as {OUTPUT_HTML}")
