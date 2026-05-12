# 🚀 NASA Space Explorer

A full-stack AI web application that integrates real-time NASA public APIs with dynamic Large Language Model (LLM) explanations. Built with Python and Streamlit, this app translates complex space data into language anyone can understand, from a curious 10-year-old to a seasoned space researcher.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![NASA](https://img.shields.io/badge/NASA_APIs-0B3D91?style=for-the-badge&logo=nasa&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_Llama_3-F55036?style=for-the-badge&logo=groq&logoColor=white)

## ✨ Features

### 📡 4 Live NASA APIs
* **Astronomy Picture of the Day (APOD):** Browse historic cosmic images and videos going all the way back to 1995.
* **Near-Earth Asteroids (NEO):** Real-time tracking of space rocks flying past Earth. Features live hazard classification, speed, and miss-distance.
* **Curiosity Rover Photos:** Actual live imagery taken on the surface of Mars, fetched directly from the rover's cameras.
* **DSCOVR EPIC Camera:** Full-disc imagery of Earth taken from a satellite 1.5 million kilometres away.

### 🤖 Adaptive AI Layer (Powered by Groq)
* **Dynamic Audience Prompting:** A single dropdown changes the AI's entire tone. Select between *10-year-old*, *High School Student*, *Science Graduate*, or *Space Researcher*, and the LLM rewrites the NASA data to match the target audience's comprehension level.
* **Dual Model Architecture:** 
  * Uses **Llama 3.3 70B** for deep, accurate scientific explanations (physics, chemistry, complex reasoning).
  * Uses **Llama 3.1 8B** for high-speed, creative tasks (e.g., writing a first-person story from the Mars rover's perspective).

### 🗄️ Full-Stack & Engineering Highlights
* **Favorites Gallery (SQLite):** A fully persistent local database allowing users to save, view, and delete their favorite NASA media. No ORM overhead, just pure Python and SQL.
* **Interactive Data Visualization:** Pandas and Altair are used to generate an interactive scatter plot of near-Earth asteroids, mapping size, speed, and hazard threat. Includes 1-click CSV data export.
* **Resilient Architecture:** Every API call is wrapped in robust 	ry/except blocks with hardcoded fallback data. If NASA servers go down, the app degrades gracefully with zero crashes.
* **Aggressive Caching:** Implements Streamlit's @st.cache_data with strict Time-To-Live (TTL) variables (3600s for live data, 86400s for daily images) to prevent API rate-limiting.

---

## 🛠️ Local Setup & Installation

### 1. Clone the repository
\\\ash
git clone https://github.com/yourusername/nasa_space_explorer.git
cd nasa_space_explorer
\\\

### 2. Create and activate a virtual environment
\\\ash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
\\\

### 3. Install dependencies
\\\ash
pip install -r requirements.txt
\\\

### 4. Setup your Environment Variables
Create a file named \.env\ in the root of the project and add your API keys:
\\\env
NASA_KEY=your_nasa_api_key_here
GROQ_KEY=your_groq_api_key_here
\\\
*(You can get a free NASA API key at [api.nasa.gov](https://api.nasa.gov/) and a Groq API key at [console.groq.com](https://console.groq.com/))*

### 5. Run the Application
\\\ash
streamlit run app.py
\\\

---

## 📝 Engineering Lessons Learned
* **Prompt Engineering is highly contextual:** Dynamically altering AI outputs based on a single audience parameter took multiple iterations to guarantee tone accuracy without losing scientific facts.
* **APIs are fragile:** Building in a production environment requires assuming APIs will fail, time out, or change schemas. 
* **Model Selection matters:** Brute-forcing everything with a 70B model causes unnecessary latency. Routing creative requests to a smaller 8B model vastly improves UX speed.
* **State Management:** Utilizing \st.session_state\ effectively resolves the classic problem of React-like rerenders forgetting previously fetched API data.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📄 License
This project is open-source and available under the MIT License.
