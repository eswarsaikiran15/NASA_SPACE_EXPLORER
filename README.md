# 🚀 NASA Space Explorer — AI Guide

> A completely free, fully featured space exploration app built with  
> **NASA Open APIs + Groq AI (Llama 3) + Streamlit**  
> **Cost: ₹0 | DSA required: None**

---

## 🌟 What This App Does

| Feature | Description |
|---|---|
| 📸 **Astronomy Picture of the Day** | Beautiful NASA space image every day + AI explanation |
| ☄️ **Asteroid Tracker** | Real near-Earth asteroids today + size comparisons + AI analysis |
| 🔴 **Mars Rover Photos** | Latest real photos from Curiosity rover on Mars |
| 🌍 **Earth from Space** | Full-disc Earth photos from DSCOVR satellite |
| 🤖 **AI Explainer** | Groq's Llama 3 explains everything for kids / students / researchers |

---

## ⚡ Setup in 5 Minutes

### Step 1 — Get Your FREE API Keys (5 minutes total)

**NASA API Key** (1 minute):
1. Go to → https://api.nasa.gov
2. Fill name + email → click "Signup"
3. Key arrives in your email instantly

**Groq API Key** (2 minutes):
1. Go to → https://console.groq.com
2. Sign up with Google
3. Click "API Keys" → "Create API Key" → copy it

---

### Step 2 — Install Python packages

Open your terminal / command prompt and run:

```bash
pip install groq streamlit requests
```

---

### Step 3 — Add Your API Keys

**Option A — Paste directly in the app sidebar** (easiest for testing)
Just open the app and paste keys in the sidebar text boxes.

**Option B — Use .env file** (recommended)
1. Rename `.env.example` to `.env`
2. Open `.env` and replace the placeholder values:

```
NASA_KEY=abc123youractualnasakey
GROQ_KEY=gsk_youractualgroqkey
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

4. Add this at the TOP of app.py (line 1):
```python
from dotenv import load_dotenv
load_dotenv()
```

---

### Step 4 — Run the App

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501` 🚀

---

## 📁 Project Structure

```
nasa_space_explorer/
│
├── app.py              ← Main application (all code here)
├── requirements.txt    ← Python packages needed
├── .env.example        ← API keys template
└── README.md           ← This file
```

---

## 🎯 How to Demo This in an Interview

1. Open the app in your browser before the interview
2. Show the **Picture of the Day** tab first — visually stunning
3. Click "Explain with AI" → show it adapting for different audiences
4. Switch to **Asteroids** tab → show the size comparisons
5. Switch to **Mars** tab → show real rover photos
6. Click the AI story button → interviewer will be impressed

**What to say:**
> "I built this using NASA's free open APIs — no cost at all.  
> The AI layer uses Groq's Llama 3 model, which is faster than ChatGPT  
> and completely free. I designed it with four features and made the AI  
> adjust its explanation based on who is reading — kids, students, or researchers."

---

## 🔧 Customize It Further (bonus features to add)

- **Date picker** — already included! Go back to any date since 1995
- **Telugu/Hindi explanation** — add language selector to the AI prompt
- **Save favourites** — add SQLite to bookmark favourite space images
- **Daily email** — use APScheduler + smtplib to email the APOD every morning
- **Quiz mode** — after AI explanation, generate a 3-question quiz

---

## 📊 APIs Used (All Free)

| API | Cost | Limit | What it provides |
|---|---|---|---|
| NASA APOD | Free | 1000/hr | Daily astronomy image |
| NASA NeoWs | Free | 1000/hr | Near-Earth asteroid data |
| NASA Mars Photos | Free | 1000/hr | Curiosity rover photos |
| NASA EPIC | Free | 1000/hr | Earth full-disc images |
| Groq Llama 3 | Free | 14,400/day | AI explanations |

---

## 💼 Jobs This Project Targets

- EdTech developer (BYJU's, Unacademy, Vedantu)
- Science content platforms
- ISRO / space-tech software teams
- Museum and education digital teams
- Any AI developer role (shows API + AI + UI skills)

---

Built with ❤️ using NASA Open APIs + Groq AI
