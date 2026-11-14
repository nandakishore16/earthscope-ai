# EarthScope AI
### An AI-Assisted Earth System Trend Detective

**NASA Space Apps Challenge 2026 | Team CosmoForge AI**

[**Live Application**](https://earthscope-ai-me4t.onrender.com/) · [**GitHub Repository**](https://github.com/nandakishore16/earthscope-ai)

---

## Overview

EarthScope AI is an interactive Earth science analysis platform that helps users explore environmental trends using NASA satellite-era reanalysis data.

Built for the NASA Space Apps Challenge 2026, the project addresses the challenge **"Be An Earth System Trend Detective!"**

It combines NASA MERRA-2 datasets, Python-based statistical analysis, interactive visualizations, and Google Gemini to investigate four questions:

- **What is changing?** — Temperature and precipitation.
- **Where is it changing?** — Regional comparisons between Chennai and Hyderabad, India.
- **How much is it changing?** — Quantified trends per decade.
- **Is the change significant?** — Statistical tests, p-values, and confidence intervals.

The objective is to make Earth science data more accessible while maintaining transparency about uncertainty and scientific limitations.

## Live Demo

**Launch EarthScope AI:** https://earthscope-ai-me4t.onrender.com/

The application is hosted on Render. The free hosting service may require additional time to start after a period of inactivity.

## Key Features

### 1. NASA Earth Science Data Integration

Uses monthly NASA MERRA-2 reanalysis data retrieved through NASA Giovanni.

Supported environmental variables:

- 2-meter air temperature (T2M).
- Corrected total precipitation (PRECTOTCORR).

### 2. Interactive Regional Comparison

Visualizes historical environmental observations for Chennai and Hyderabad over the period 2005–2025.

Interactive Plotly graphs display annual observations alongside fitted linear trends.

### 3. Statistical Trend Detection

The Python analysis engine calculates:

- Annual temperature means and precipitation totals.
- Linear regression trends per decade.
- 95% confidence intervals.
- Regression p-values.
- Statistical significance at a 0.05 threshold.
- Exploratory differences between regional trends.

### 4. Gemini AI Scientific Analyst

Google Gemini generates natural-language explanations using the statistical results calculated by Python.

The AI component is designed to explain the findings, distinguish significant from nonsignificant trends, and communicate analytical limitations.

The language model does not independently calculate the scientific measurements or regression statistics.

### 5. Accessible Web Interface

Built using Gradio, allowing users to switch between environmental variables and explore results without writing Python code.

## Data Sources

| Variable | NASA dataset | Measurement |
|---|---|---|
| Air temperature | M2TMNXSLV | T2M |
| Corrected precipitation | M2TMNXFLX | PRECTOTCORR |

**Data provider:** NASA Global Modeling and Assimilation Office (GMAO), distributed through NASA GES DISC and Giovanni.

**Analysis period:** January 2005 – December 2025.

**Geographical coverage:** Selected MERRA-2 grid locations representing the Chennai and Hyderabad areas.

The repository includes four original Giovanni CSV exports in the `data/` directory. Their metadata records the user-selected and actual data bounding boxes.

### Data Processing

**Temperature**

Monthly temperature measurements are converted from Kelvin to Celsius. The application calculates the arithmetic mean of the 12 monthly values for each complete year.

**Precipitation**

Monthly corrected precipitation rates are converted from kg/m²/s (numerically equivalent to mm/s) into monthly precipitation totals using the actual number of seconds in each calendar month. Monthly totals are then summed to calculate annual precipitation.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Data processing | Pandas, NumPy |
| Statistical analysis | SciPy |
| Interactive visualization | Plotly |
| Web application | Gradio |
| AI-powered explanations | Google Gemini |
| Deployment | Render |
| Source control | GitHub |

## System Architecture

**NASA Giovanni / MERRA-2 Data**

↓

**Data Ingestion and Preprocessing**

↓

**Python Statistical Analysis Engine**

↓

**Trend Detection and Regional Comparison**

↓

**Interactive Gradio Dashboard**

↓

**Gemini AI Scientific Analyst**

The statistical analysis engine produces the numerical results. Gemini receives summarized findings and generates interpretive explanations.

## Project Structure

```text
earthscope-ai/
├── app.py
├── analysis.py
├── ai_analyst.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    ├── chennai_temperature.csv
    ├── hyderabad_temperature.csv
    ├── chennai_precipitation.csv
    └── hyderabad_precipitation.csv
```

**File responsibilities**

- `app.py` — Gradio dashboard and visualization.
- `analysis.py` — NASA CSV processing and statistical analysis.
- `ai_analyst.py` — Gemini-powered scientific interpretation.
- `data/` — NASA Giovanni CSV exports.
- `requirements.txt` — Python dependencies.

## Running Locally

### Prerequisites

- Python 3.10 or later, with a compatible dependency environment.
- Internet connection for Gemini requests.
- Google Gemini API key for AI explanations.

### 1. Clone the repository

```bash
git clone https://github.com/nandakishore16/earthscope-ai.git
cd earthscope-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini

Create a `.env` file in the project directory:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Keep your API key private. Never commit `.env` to a public repository.

### 4. Start the application

```bash
python app.py
```

Open:

http://127.0.0.1:7860

### 5. Explore the dashboard

1. Select Temperature or Precipitation.
2. Examine the annual observations and fitted trends.
3. Review the regional statistical comparison.
4. Click **Generate AI explanation** to obtain a natural-language interpretation.

The statistical dashboard can operate without Gemini, but AI explanations require a valid API key.

## Scientific Methodology

For each region and environmental variable, the application aggregates monthly observations into annual measurements.

Ordinary least squares regression is applied to the annual time series to estimate the linear trend.

The trend is expressed per decade. Conventional 95% confidence intervals and regression p-values are calculated using SciPy.

A p-value below 0.05 is reported as statistically significant under the regression assumptions.

The application also estimates differences in trends between Chennai and Hyderabad using paired annual observations.

## Scientific Limitations

EarthScope AI is an exploratory scientific analysis prototype, not a substitute for a comprehensive climate assessment.

Important limitations include:

- MERRA-2 is a coarse-resolution reanalysis product, not a direct measurement from city weather stations.
- The current application covers two selected regions and two environmental variables.
- The analysis uses 21 complete annual observations from 2005–2025.
- Conventional regression p-values do not account for temporal autocorrelation.
- Monthly temperature values are averaged without weighting by the number of days in each month.
- A nonsignificant trend does not prove that environmental change is absent.
- Differences between regions do not establish causal relationships.
- Gemini-generated explanations may contain errors and should be checked against the reported statistics.

Future scientific improvements could include seasonal trend analysis, autocorrelation-aware inference, additional uncertainty estimates, and independent dataset validation.

## Future Enhancements

Potential extensions include:

- User-defined geographical regions.
- Additional NASA Earth science variables.
- Interactive geographical trend maps.
- Seasonal and anomaly-based analysis.
- More robust statistical significance testing.
- Automated data retrieval.
- Exportable scientific reports.

These features are proposed improvements and are not part of the current deployed prototype.

## AI Usage Disclosure

EarthScope AI uses Google Gemini to generate natural-language explanations of statistics calculated by Python.

Generative AI assistance was also used during project development, including code generation, debugging, documentation, and written descriptions.

AI-generated explanations are interpretive and are not presented as independently validated scientific conclusions.

## References and Attribution

- [NASA Giovanni](https://giovanni.gsfc.nasa.gov/giovanni/)
- [NASA MERRA-2](https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/)
- [NASA GES DISC](https://disc.gsfc.nasa.gov/)
- [Google AI for Developers](https://ai.google.dev/)
- [Gradio](https://www.gradio.app/)
- [SciPy](https://scipy.org/)
- [Plotly](https://plotly.com/python/)

NASA data and associated scientific products are credited to their respective providers. The project is an independent hackathon prototype and is not an official NASA application.

## Hackathon Information

**Event:** NASA Space Apps Challenge 2026

**Challenge:** Be An Earth System Trend Detective!

**Team:** CosmoForge AI

**Project:** EarthScope AI

**Source Code:** https://github.com/nandakishore16/earthscope-ai

**Live Application:** https://earthscope-ai-me4t.onrender.com/

---

*Explore NASA data. Detect trends. Understand uncertainty.*
