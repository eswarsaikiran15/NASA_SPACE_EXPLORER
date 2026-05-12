# 🚀 NASA Space Explorer

A full-stack AI web application that integrates real-time NASA public APIs with dynamic Large Language Model (LLM) explanations. Built with Python and Streamlit, this app translates complex space data into language anyone can understand, from a curious 10-year-old to a seasoned space researcher.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![NASA](https://img.shields.io/badge/NASA_APIs-0B3D91?style=for-the-badge&logo=nasa&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_Llama_3-F55036?style=for-the-badge&logo=groq&logoColor=white)

---


## 🌌 Project Overview

Space is fascinating, but raw NASA data is often wrapped in heavy scientific jargon. **NASA Space Explorer** bridges this gap. It fetches live, real-world data from four distinct NASA APIs and routes it through Groq-powered LLMs (Llama 3). 

Users simply select an target audience from a dropdown—ranging from a 10-year-old child to a space researcher—and the application dynamically adjusts everything it explains, providing custom-tailored planetary stories, asteroid hazard analyses, and astronomical deep-dives.

---

## 🏗 Architecture & Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/)
* **Backend:** Pure Python 3
* **Database:** SQLite (built-in, via `sqlite3`)
* **AI Provider:** [Groq](https://groq.com/) API (Llama 3.3 70B & Llama 3.1 8B)
* **Data Sources:** [NASA Open APIs](https://api.nasa.gov/)
* **Data Visualization:** Pandas + Altair

### 📂 Project Structure
```text
nasa_space_explorer/
│
├── app.py              # Main Streamlit application and API logic
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API keys
├── .gitignore          # Files ignored by git
└── README.md           # Project documentation
```

---

## ✨ Key Features

### 📡 1. The Data Layer (4 Live NASA APIs)
* **Astronomy Picture of the Day (APOD):** Browse historic cosmic images and videos going all the way back to 1995.
* **Near-Earth Asteroids (NEO):** Real-time tracking of space rocks flying past Earth today.
* **Curiosity Rover Photos:** Actual live imagery taken on the surface of Mars.
* **DSCOVR EPIC Camera:** Full-disc imagery of Earth taken from a satellite 1.5 million kilometres away.

### 🤖 2. The AI Layer (Adaptive LLMs)
* **Audience-Driven Dynamic Prompting:** The AI entirely changes its tone, vocabulary, and depth based on a single variable (e.g., emojis and analogies for kids, raw physics and statistics for researchers).
* **Targeted Model Selection:** 
  * Uses **Llama-3.3-70B-Versatile** for deep, accurate scientific explanations.
  * Uses **Llama-3.1-8B-Instant** for high-speed, creative tasks (like generating first-person POV stories from the Mars rover).

### 🗄️ 3. The Application Layer
* **Favorites Gallery (SQLite Database):** Users can save APOD objects to a persistent local SQL database and manage them via a full CRUD interface.
* **Interactive Altair Charts:** Transforming raw API objects into an interactive scatter plot where bubbles map out asteroid size, speed, and hazard threat.
* **Resilient Fallbacks:** `try/except` wrappers around all external network calls prevent crashes. If NASA servers have downtime, the app gracefully provides cached/static data.

---

## 🛠️ Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/nasa_space_explorer.git
cd nasa_space_explorer
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup your Environment Variables
Create a file named `.env` in the root of the project:
```env
NASA_KEY=your_nasa_api_key_here
GROQ_KEY=your_groq_api_key_here
```
*(Grab a free NASA Key [here](https://api.nasa.gov/) and a free Groq Key [here](https://console.groq.com/))*

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 📝 Engineering Lessons Learned
Building this pushed me out of "tutorial hell" into dealing with real engineering problems:
1. **APIs break:** You must build for failure. Implementing fallback static data keeps users engaged when external services go offline.
2. **LLM formatting is unpredictable:** Model selection matters. Use 70B parameters for complex reasoning, but 8B parameters for immediate creative tasks to optimize UX load times.
3. **Prompt Architecture:** Designing a prompt that seamlessly scales from "childish analogies" to "post-grad astrophysics" required extensive iteration.
4. **State Management:** Overcoming the ephemeral nature of standard dashboard scripts meant mastering `st.session_state` so users don't lose data upon clicking an interactive button.

---

## 🚀 Future Improvements
- [ ] Add Authentication to allow multiple users to have separate "Favorite Galleries".
- [ ] Migrate SQLite to PostgreSQL or Supabase for a fully deployed cloud-hosted version.
- [ ] Add the James Webb Space Telescope (JWST) API for deeper infra-red space imagery.
- [ ] Cache LLM explanations in the database to reduce Groq API calls over time.

