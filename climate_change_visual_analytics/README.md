# Climate Change — Visual Analytics Final Project


**Course:** Data Visualization for Data Science
**Theme:** Climate & Weather (Berkeley Earth Surface Temperature Study)

---

## Research Question

> *In this project, we investigate whether the industrial era influences global land surface temperature patterns using real-world data.*

---

## Folder Contents

```
.
├── README.md                                ← Current File
├── Climate_Final_Project.ipynb              ← main analysis notebook
├── dashboard.py                             ← Streamlit interactive dashboard
└── data/
    ├── GlobalTemperatures.csv
    ├── GlobalLandTemperaturesByCountry.csv
    └── GlobalLandTemperaturesByMajorCity.csv
```

---

## Setup

Open a terminal in this folder and create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac / Linux
pip install pandas numpy matplotlib seaborn plotly streamlit jupyter ipykernel
```

---

## How to Run the Notebook

Open `Climate_Final_Project.ipynb` in Jupyter or VS Code, select the `.venv` kernel, and click **Run All**. All ten visualizations and the interactive Plotly choropleth will render.

---

## How to Run the Dashboard

From the same terminal (with the virtual environment active):

```bash
streamlit run dashboard.py
```

A browser tab opens automatically at `http://localhost:8501`. The dashboard has:

- **Country dropdown** — explore any of 242 countries
- **Year-range slider** — focus on any window between 1850 and 2013
- **Smoothing slider** — control the rolling-mean window
- **Four linked charts** that update together when any control changes

Press `Ctrl + C` in the terminal to stop the dashboard.

---

## Project Structure

The notebook follows the required storytelling structure:

1. Problem statement
2. Data overview
3. Visual exploration (10 visualizations + 1 interactive Plotly choropleth)
4. Key insights
5. Decision recommendations

The 3-page report and 14-slide presentation summarize the findings for non-technical readers.

---

## Data Source

Berkeley Earth Surface Temperature Study, accessed via Kaggle:
https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

The CSVs are bundled in the `data/` folder so the notebook and dashboard run out of the box — no Kaggle account or download required.
