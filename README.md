# Tactical Soccer Dashboard ⚽

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
streamlit run app.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`.

## Usage
1. Enter a valid **WhoScored Match ID**, along with the League and Season.
2. Click **Generate Maps**.
3. Use the sidebar to filter times, toggle substitutes, or change themes!
