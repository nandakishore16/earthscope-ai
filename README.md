# EarthScope AI — Phase 3

NASA Space Apps Challenge 2026 · CosmoForge AI

## Run

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:7860. Select **Temperature** or **Precipitation**.

## Data and method

Four unmodified NASA Giovanni CSV exports are included under `data/`: monthly MERRA-2 `T2M` and `PRECTOTCORR` for two user-defined bounding boxes. Metadata in each file records both requested and actual spatial coverage.

Temperature is converted from Kelvin to Celsius and averaged across 12 months per complete year. Corrected precipitation is a monthly mean rate in kg m⁻² s⁻¹, numerically equivalent to mm/s. Multiply by actual seconds in each calendar month to obtain monthly totals, then sum by year. Annual trends are fitted with ordinary least squares; confidence intervals and p-values assume independent errors and are exploratory. Coarse reanalysis cells are not direct city observations.

## Attribution

NASA Goddard Earth Sciences Data and Information Services Center (GES DISC), Giovanni; NASA MERRA-2 reanalysis. Python, pandas, SciPy, Plotly and Gradio. Source CSVs contain Giovanni reproduction URLs.

## Phase 4: optional Gemini AI Scientific Analyst

1. Install packages: `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env` in the `earthscope_ai` folder.
3. Set `GEMINI_API_KEY` to your Google AI Studio key. Never publish `.env`.
4. Run `python app.py` and open `http://127.0.0.1:7860`.
5. Choose Temperature or Precipitation, then click **Generate AI explanation**.

The statistical results are computed entirely in Python. Gemini receives only the summarized statistics, not raw data or the API key. Model responses are interpretive, not authoritative scientific conclusions. The default model is `gemini-2.5-flash`; set `GEMINI_MODEL` in `.env` if it is unavailable for your account.
