# Tactical Soccer Dashboard ⚽

# 🚨 לרועי: מדריך הפעלה מדויק מ-0 (בלי תקלות!)
**השגיאה שקיבלת קודם קרתה כי בטעות העתקת גם את התו `>` לטרמינל!**
כדי לעשות סדר ולגרום לזה לעבוד בצורה חלקה, עשה בדיוק את הצעדים הבאים:

1. פתח טרמינל (PowerShell) וודא שאתה בנתיב הראשי של הפרויקט:
```powershell
cd C:\Users\Roei\Desktop\soccer_project
```

2. הפעל את הסביבה הוירטואלית התקינה שיצרנו בהתחלה:
```powershell
.\.venv\Scripts\activate
```

3. היכנס לתיקייה של האפליקציה:
```powershell
cd .venv\web_app
```

4. עכשיו, פשוט תריץ (תעתיק בלי תווים מיותרים):
```powershell
streamlit run app.py
```

זה הכל! האפליקציה תידלק מיד.
(ד"א, מומלץ למחוק את התיקייה בשם `.venv` שנמצאת בטעות בתוך `web_app` כדי שהיא לא תעשה לך התנגשויות בעתיד).

A powerful, interactive web application built with Streamlit to analyze football match data dynamically.

## Features
- **Time Filtering:** Analyze match events by selecting specific minute ranges dynamically.
- **Passing Networks:** Visualize team passing combinations, pass volumes, and central hubs.
- **Pass Sonars 📡:** Radar-style wedges showing directional passing tendencies for each player.
- **Team Shape 🛡️:** Convex hull visualizations showing the outfield shape (width, height, and line height).
- **Shot Maps:** Map of all shots and goals.
- **Heatmaps:** Density maps showing where a team controlled the game.
- **Time-lapse Animation 🎬:** Automatically generate an animated GIF of the passing network over 15-minute intervals.
- **High-Quality Export:** One-click downloads for every visualization generated.

## Prerequisites
Make sure you have Python installed (3.8+ recommended).

## Installation

1. Clone this repository:
```bash
git clone https://github.com/roiky/Passmap_webapp.git
cd Passmap_webapp
```

2. Create a virtual environment (optional but highly recommended):
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Mac/Linux:
source .venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

Start the Streamlit application by running the following command in your terminal:
```bash
python -m streamlit run app.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`.

## Usage
1. Enter a valid **WhoScored Match ID**, along with the League and Season.
2. Click **Generate Maps**.
3. Use the sidebar to filter times, toggle substitutes, or change themes!
