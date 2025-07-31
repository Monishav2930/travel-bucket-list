import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="🧙 Marauder's Travel Bucket List", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #1a1a1a;
            color: #f0e130;
        }
        .title {
            font-size: 2.5em;
            color: #f0e130;
            text-shadow: 0 0 10px #f0e130;
        }
        .sparkle {
            animation: sparkle 1.5s infinite alternate;
        }
        @keyframes sparkle {
            from {text-shadow: 0 0 5px #f0e130;}
            to {text-shadow: 0 0 20px #fff700, 0 0 30px #f0e130;}
        }
        .destination-card {
            background-color: #2e2e2e;
            border: 2px solid #f0e130;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title sparkle'>🧙 Marauder's Travel Bucket List</h1>", unsafe_allow_html=True)


if 'destinations' not in st.session_state:
    st.session_state.destinations = []

with st.form("add_destination"):
    st.markdown("## ⚡ Add a Magical Destination")
    name = st.text_input("Place Name (e.g. Manali, India)")
    description = st.text_area("Short Description")
    image_url = st.text_input("Image URL (optional)")
    submitted = st.form_submit_button("Add to Bucket List")

    if submitted and name and description:
        geolocator = Nominatim(user_agent="magic_map_app")
        location = geolocator.geocode(name)
        if location:
            st.session_state.destinations.append({
                "name": name,
                "description": description,
                "image_url": image_url,
                "latitude": location.latitude,
                "longitude": location.longitude
            })
            st.success(f"✨ {name} added to your magical bucket list!")
        else:
            st.error("Location not found. Please try a more specific place name.")

st.markdown("## 🪄 Your Magical Bucket List")

for i, place in enumerate(st.session_state.destinations):
    with st.container():
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            if st.button("❌", key=f"del_{i}", help="Delete this place"):
                st.session_state.destinations.pop(i)
                st.experimental_rerun()
        with col2:
            st.markdown(f"""
            <div class='destination-card'>
                <h3 class='sparkle'>{place['name']}</h3>
                <p>{place['description']}</p>
                {f'<img src="{place["image_url"]}" width="100%" style="border-radius:8px; margin-bottom:10px;">' if place["image_url"] else ""}
                <p><a href="https://www.google.com/maps/search/?api=1&query={place['latitude']},{place['longitude']}" target="_blank">🗺️ View on Google Maps</a></p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("## 🧭 Magical Marauder's Map")

map_center = [20.5937, 78.9629]  
m = folium.Map(location=map_center, zoom_start=4, tiles='cartodbpositron')

for place in st.session_state.destinations:
    folium.Marker(
        [place['latitude'], place['longitude']],
        popup=place['name'],
        tooltip=place['description']
    ).add_to(m)

st_folium(m, width=700, height=500)
