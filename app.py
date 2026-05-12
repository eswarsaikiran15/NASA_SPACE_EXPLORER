import streamlit as st
import requests
from groq import Groq
from datetime import date, timedelta
import os
import sqlite3
import pandas as pd
import altair as alt
from dotenv import load_dotenv

load_dotenv()  # Load API keys from .env file

# ── DATABASE INIT ──────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('favorites.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS favorites
                 (date TEXT PRIMARY KEY, title TEXT, url TEXT, explanation TEXT, media_type TEXT)''')
    conn.commit()
    conn.close()

def add_favorite(fav_date, title, url, explanation, media_type):
    conn = sqlite3.connect('favorites.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO favorites VALUES (?, ?, ?, ?, ?)", (fav_date, title, url, explanation, media_type))
    conn.commit()
    conn.close()

def get_favorites():
    conn = sqlite3.connect('favorites.db')
    df = pd.read_sql_query("SELECT * FROM favorites ORDER BY date DESC", conn)
    conn.close()
    return df

def remove_favorite(fav_date):
    conn = sqlite3.connect('favorites.db')
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE date = ?", (fav_date,))
    conn.commit()
    conn.close()

init_db()

# ── CONFIG ─────────────────────────────────────────────────────────────────────
NASA_KEY  = os.getenv("NASA_KEY",  "YOUR_NASA_KEY")   # api.nasa.gov
GROQ_KEY  = os.getenv("GROQ_KEY",  "YOUR_GROQ_KEY")   # console.groq.com
client    = Groq(api_key=GROQ_KEY)

st.set_page_config(
    page_title="🚀 NASA Space Explorer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🚀 NASA Space Explorer")
    st.caption("Built with NASA API + Groq AI")
    st.divider()

    audience = st.selectbox(
        "🎯 Explain for...",
        ["curious 10-year-old", "high school student", "science graduate", "space researcher"],
        help="AI will adjust its language based on who is reading"
    )


# ── HELPER: GROQ ───────────────────────────────────────────────────────────────
def ai_explain(text: str, audience: str, context: str = "") -> str:
    system = (
        "You are an enthusiastic space scientist who loves making astronomy "
        "exciting and accessible. You adjust your language perfectly for your audience."
    )
    user_prompt = f"""
Explain the following for a {audience}.
{f"Context: {context}" if context else ""}

Content to explain:
{text}

Guidelines:
- For a 10-year-old: use fun analogies, emojis, short sentences, avoid jargon
- For a high school student: use some science terms, explain them, make it engaging
- For a science graduate: use proper terminology, go deeper into physics/chemistry
- For a space researcher: be technical, mention relevant data, open questions

End with one "Fun Fact 🌟" relevant to the topic.
Keep response under 300 words.
"""
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user_prompt}
        ]
    )
    return res.choices[0].message.content


def ai_compare_asteroids(asteroids: list, audience: str) -> str:
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"""
These asteroids are flying near Earth today:
{asteroids}

For a {audience}:
1. Explain what near-Earth objects are
2. Put the sizes in perspective (compare to buildings, cities, etc.)
3. Are any of them dangerous? Explain clearly
4. How do scientists track these?
Keep it under 250 words and engaging.
"""}]
    )
    return res.choices[0].message.content


def ai_mars_story(photos: list, audience: str) -> str:
    descriptions = [f"Photo taken on {p['earth_date']} by {p['camera']['full_name']} camera, Sol {p['sol']}" for p in photos]
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"""
These are real photos taken by NASA's Curiosity rover on Mars:
{descriptions}

For a {audience}, write an exciting 150-word story about what the rover might be "seeing" and "thinking" as it explores Mars.
Make it first-person from the rover's perspective. Be scientifically accurate but fun.
"""}]
    )
    return res.choices[0].message.content


# ── API CALLS ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def get_apod(chosen_date: str = ""):
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}"
    if chosen_date:
        url += f"&date={chosen_date}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@st.cache_data(ttl=3600)
def get_asteroids(target_date=None):
    if target_date is None:
        target_date = date.today()
    
    date_str = target_date.isoformat()
    url   = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={date_str}&end_date={date_str}&api_key={NASA_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data  = response.json()
        all_objects = []
        for day_objects in data.get("near_earth_objects", {}).values():
            all_objects.extend(day_objects)
        result = []
        for o in all_objects[:6]:
            result.append({
                "name":       o["name"],
                "diameter_km": round(o["estimated_diameter"]["kilometers"]["estimated_diameter_max"], 3),
                "diameter_m":  round(o["estimated_diameter"]["meters"]["estimated_diameter_max"],     1),
                "hazardous":  o["is_potentially_hazardous_asteroid"],
                "speed_kmh":  round(float(o["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]), 0),
                "miss_km":    round(float(o["close_approach_data"][0]["miss_distance"]["kilometers"]), 0),
            })
        return result
    except Exception as e:
        return []


@st.cache_data(ttl=3600)
def get_mars_photos(target_date=None):
    if target_date is None:
        target_date = date.today()
    date_str = target_date.isoformat()
    # Try the specific date first, if empty, it'll fall back naturally
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={date_str}&api_key={NASA_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        photos = data.get("photos", [])
        if not photos: # If no photos for exact date, get latest
            url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={NASA_KEY}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            photos = data.get("latest_photos", [])
        return photos[:6]
    except Exception as e:
        # Fallback to static data when NASA API is down
        return [
            {
                "img_src": "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FLB_486265257EDR_F0481570FHAZ00323M_.JPG",
                "earth_date": "2015-05-30",
                "sol": 1000,
                "camera": {"full_name": "Front Hazard Avoidance Camera (Fallback Data)"}
            },
            {
                "img_src": "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/rcam/RLB_486265291EDR_F0481570RHAZ00323M_.JPG",
                "earth_date": "2015-05-30",
                "sol": 1000,
                "camera": {"full_name": "Rear Hazard Avoidance Camera (Fallback Data)"}
            }
        ]


@st.cache_data(ttl=86400)
def get_epic_image(target_date=None):
    if target_date is None:
        target_date = date.today()
    date_str = target_date.isoformat()
    # Try fetching images specifically for the selected date
    url  = f"https://api.nasa.gov/EPIC/api/natural/date/{date_str}?api_key={NASA_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # If no images on that exact date, get the most recent ones
        if not data or len(data) == 0:
             url  = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={NASA_KEY}"
             response = requests.get(url, timeout=10)
             response.raise_for_status()
             data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            img  = data[0]
            date_str = img["date"][:10].replace("-", "/")
            img_url  = f"https://epic.gsfc.nasa.gov/archive/natural/{date_str}/png/{img['image']}.png"
            return img_url, img["caption"], img["date"]
        return None, None, None
    except Exception as e:
        # Fallback to static data when NASA API is down
        return (
            "https://epic.gsfc.nasa.gov/archive/natural/2015/10/31/png/epic_1b_20151031074844.png", 
            "Earth as seen by the DSCOVR satellite (Fallback image due to NASA API outage)", 
            "2015-10-31"
        )


# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 Picture of the Day",
    "☄️ Asteroids Today",
    "🔴 Mars Rover",
    "🌍 Earth from Space",
    "⭐ Favorites Gallery"
])


# ── TAB 1: APOD ────────────────────────────────────────────────────────────────
with tab1:
    st.header("Astronomy Picture of the Day")

    col_date, col_btn = st.columns([2, 1])
    with col_date:
        chosen_date = st.date_input(
            "Pick any date (NASA has photos from 1995!)",
            value=date.today(),
            min_value=date(1995, 6, 16),
            max_value=date.today()
        )
    with col_btn:
        st.write("")
        st.write("")
        load_btn = st.button("🔭 Load Photo")

    # Load new photo if button is clicked OR if it's the first time
    if load_btn or "apod" not in st.session_state:
        with st.spinner("Fetching from NASA..."):
            st.session_state.apod = get_apod(str(chosen_date))
            st.session_state.last_date = chosen_date

    # If the user changed the date but didn't click load, let's load it automatically
    elif "last_date" in st.session_state and st.session_state.last_date != chosen_date:
        with st.spinner("Fetching from NASA..."):
            st.session_state.apod = get_apod(str(chosen_date))
            st.session_state.last_date = chosen_date

    apod = st.session_state.get("apod", {})

    if apod and "url" in apod:
        st.subheader(apod.get("title", ""))
        media_type = apod.get("media_type", "image")

        if media_type == "image":
            st.image(apod["url"])
        elif media_type == "video":
            st.video(apod["url"])
            st.caption("📹 Today's APOD is a video")

        with st.expander("📝 NASA's Original Description"):
            st.write(apod.get("explanation", "No description available."))
            if apod.get("copyright"):
                st.caption(f"📷 Credit: {apod['copyright']}")

        st.divider()
        col_ai, col_fav = st.columns(2)
        with col_ai:
            if st.button("🤖 Explain with AI", key="explain_apod", use_container_width=True):
                with st.spinner(f"AI is explaining for a {audience}..."):
                    explanation = ai_explain(
                        apod.get("explanation", ""),
                        audience,
                        context=f"The image title is: {apod.get('title', '')}"
                    )
                st.success("AI Explanation")
                st.write(explanation)
        with col_fav:
            if st.button("❤️ Save to Favorites", use_container_width=True):
                add_favorite(
                    str(chosen_date), 
                    apod.get("title", ""), 
                    apod.get("url", ""), 
                    apod.get("explanation", ""), 
                    media_type
                )
                st.success("✨ Saved to your Favorites Gallery!")
    else:
        st.error("Could not load APOD. Check your NASA API key.")
        if apod:
            st.json(apod)


# ── TAB 2: ASTEROIDS ───────────────────────────────────────────────────────────
with tab2:
    # Use the chosen_date from Tab 1 so the asteroid date matches the APOD date
    display_date = chosen_date if 'chosen_date' in locals() else date.today()
    st.header(f"☄️ Near-Earth Asteroids — {display_date.strftime('%B %d, %Y')}")

    with st.spinner("Fetching asteroid data from NASA..."):
        asteroids = get_asteroids(display_date)

    if asteroids:
        hazardous   = [a for a in asteroids if a["hazardous"]]
        safe        = [a for a in asteroids if not a["hazardous"]]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tracked Today", len(asteroids))
        col2.metric("⚠️ Potentially Hazardous", len(hazardous), delta=None)
        col3.metric("✅ Safe Objects", len(safe))

        st.divider()

        st.subheader("📊 Asteroid Analysis")
        # Convert asteroid data to pandas DataFrame for Altair chart
        if len(asteroids) > 0:
            df = pd.DataFrame(asteroids)
            
            c_head, c_download = st.columns([3, 1])
            with c_download:
                st.download_button(
                    label="💾 Download Data (CSV)",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name=f"nasa_asteroids_{display_date}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Interactive scatter plot with Altair
            chart = alt.Chart(df).mark_circle().encode(
                x=alt.X('miss_km:Q', title='Miss Distance (km)', scale=alt.Scale(zero=False)),
                y=alt.Y('speed_kmh:Q', title='Speed (km/h)', scale=alt.Scale(zero=False)),
                size=alt.Size('diameter_m:Q', title='Diameter (m)', scale=alt.Scale(range=[100, 1000])),
                color=alt.Color('hazardous:N', title='Hazardous', scale=alt.Scale(domain=[True, False], range=['red', 'green'])),
                tooltip=['name', 'diameter_m', 'speed_kmh', 'miss_km', 'hazardous']
            ).interactive().properties(height=400)
            
            st.altair_chart(chart, use_container_width=True)
            st.caption("🔍 Hover over the bubbles to see details. You can zoom and pan the chart!")

        st.divider()

        for a in asteroids:
            icon  = "⚠️" if a["hazardous"] else "✅"
            label = "POTENTIALLY HAZARDOUS" if a["hazardous"] else "Safe"
            color = "🔴" if a["hazardous"] else "🟢"

            with st.expander(f"{icon} {a['name']} — {a['diameter_m']} metres wide"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Diameter", f"{a['diameter_m']} m")
                c2.metric("Speed", f"{int(a['speed_kmh']):,} km/h")
                c3.metric("Miss Distance", f"{int(a['miss_km']):,} km")
                c4.metric("Status", label)

                # Size comparison
                size = a["diameter_m"]
                if size < 50:
                    compare = "🏠 About the size of a large house"
                elif size < 150:
                    compare = "🏟️ About the size of a cricket stadium"
                elif size < 500:
                    compare = "🏙️ As wide as several city blocks"
                else:
                    compare = "🏔️ As big as a small mountain"
                st.caption(compare)

        st.divider()
        if st.button("🤖 AI: Explain these asteroids"):
            with st.spinner("AI is analysing the asteroids..."):
                explanation = ai_compare_asteroids(asteroids, audience)
            st.write(explanation)
    else:
        st.warning("No asteroid data available. Check your NASA API key.")


# ── TAB 3: MARS ────────────────────────────────────────────────────────────────
with tab3:
    display_date = chosen_date if 'chosen_date' in locals() else date.today()
    st.header("🔴 Mars — Curiosity Rover's Photos")
    st.caption(f"Real photos taken on Mars, near {display_date.strftime('%B %d, %Y')}")

    with st.spinner("Fetching Mars photos..."):
        mars_photos = get_mars_photos(display_date)

    if mars_photos:
        photo_date = mars_photos[0].get("earth_date", "Unknown")
        sol        = mars_photos[0].get("sol", "?")
        st.info(f"📅 Photos from Earth Date: **{photo_date}** | Martian Sol: **{sol}**")

        cols = st.columns(3)
        for i, photo in enumerate(mars_photos[:6]):
            with cols[i % 3]:
                st.image(photo["img_src"], caption=photo["camera"]["full_name"])

        st.divider()
        if st.button("🤖 AI: Write a story from the rover's perspective"):
            with st.spinner("AI is writing a Mars story..."):
                story = ai_mars_story(mars_photos, audience)
            st.write(story)

        with st.expander("📋 Photo Details"):
            for p in mars_photos[:3]:
                st.write(f"**Camera:** {p['camera']['full_name']} | **Date:** {p['earth_date']} | **Sol:** {p['sol']}")
    else:
        st.warning("Could not load Mars photos. NASA's Mars API might be temporarily down or your API key is invalid.")


# ── TAB 4: EPIC ────────────────────────────────────────────────────────────────
with tab4:
    display_date = chosen_date if 'chosen_date' in locals() else date.today()
    st.header("🌍 Earth from Space — NASA EPIC Camera")
    st.caption(f"Photos of Earth taken from 1.5 million km away around {display_date.strftime('%B %d, %Y')}")

    with st.spinner("Fetching Earth image..."):
        epic_url, epic_caption, epic_date = get_epic_image(display_date)

    if epic_url:
        st.image(epic_url, caption=f"Earth as seen from space — {epic_date}")

        with st.expander("📝 Photo Details"):
            st.write(epic_caption)

        if st.button("🤖 AI: What can scientists learn from this photo?"):
            with st.spinner("AI is analysing..."):
                explanation = ai_explain(
                    epic_caption or "A full-disc image of Earth taken from 1.5 million km away by the DSCOVR EPIC camera.",
                    audience,
                    context="This is a full-disc image of Earth from space"
                )
            st.write(explanation)
    else:
        st.warning("Could not load EPIC image. Try again later or check your NASA API key.")


# ── TAB 5: FAVORITES GALLERY ───────────────────────────────────────────────────
with tab5:
    st.header("⭐ Your Favorites Gallery")
    st.caption("All the APOD images you've saved locally")
    
    fav_df = get_favorites()
    
    if fav_df.empty:
        st.info("You haven't saved any favorites yet! Go to the 'Picture of the Day' tab and click '❤️ Save to Favorites'.")
    else:
        # Create a grid for the gallery
        cols = st.columns(3)
        for idx, row in fav_df.iterrows():
            with cols[idx % 3]:
                st.subheader(row['date'])
                if row['media_type'] == 'image':
                    st.image(row['url'], use_container_width=True)
                else:
                    st.video(row['url'])
                with st.expander(row['title']):
                    st.write(row['explanation'])
                    if st.button("🗑️ Remove", key=f"del_{row['date']}", use_container_width=True):
                        remove_favorite(row['date'])
                        st.rerun()


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.divider()
st.caption("🚀 Built with NASA Open APIs + Groq AI (Llama 3) + Streamlit · Data from NASA · AI by Groq · ₹0 cost")
