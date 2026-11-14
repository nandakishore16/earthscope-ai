from pathlib import Path
import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
from analysis import load_giovanni, analyze
from ai_analyst import explain

DATA = Path(__file__).resolve().parent / 'data'
CITIES = ('Chennai', 'Hyderabad')


def compare(variable):
    unit = '°C' if variable == 'Temperature' else 'mm'
    unit_decade = f'{unit}/decade'
    figure = go.Figure()
    rows, notes, series = [], [], {}
    ai_rows = []
    for city in CITIES:
        path = DATA / f'{city.lower()}_{variable.lower()}.csv'
        df, metadata = load_giovanni(path, variable)
        annual, r = analyze(df, variable)
        series[city] = annual
        figure.add_trace(go.Scatter(x=annual.year, y=annual.measurement,
            mode='lines+markers', name=f'{city}: annual observed'))
        figure.add_trace(go.Scatter(x=annual.year, y=annual.fitted,
            mode='lines', line=dict(dash='dash'), name=f'{city}: linear fit'))
        rows.append({'Region':city, 'Complete years':r['n_years'],
            f'Trend ({unit_decade})':round(r['slope_decade'],3),
            '95% CI lower':round(r['ci_low'],3),
            '95% CI upper':round(r['ci_high'],3),
            'Regression p-value':round(r['p_value'],5),
            'Significant (p < 0.05)':r['significant'],
            'User bounding box':metadata.get('User Bounding Box',''),
            'Data bounding box':metadata.get('Data Bounding Box','')})
        ai_rows.append({'region': city, 'complete_years': r['n_years'], 'trend_per_decade': round(r['slope_decade'], 5), 'ci_low': round(r['ci_low'], 5), 'ci_high': round(r['ci_high'], 5), 'p_value': round(r['p_value'], 6), 'significant_at_0_05': r['significant'], 'unit': unit_decade, 'data_bounding_box': metadata.get('Data Bounding Box', '')})
        notes.append(f"**{city}:** {r['slope_decade']:+.3f} {unit_decade}; p={r['p_value']:.4f}; "
                     + ('significant' if r['significant'] else 'not statistically significant') + ' at α=0.05.')
    matched = series['Chennai'][['year','measurement']].merge(
        series['Hyderabad'][['year','measurement']],on='year',suffixes=('_chennai','_hyderabad'))
    fit = stats.linregress(matched.year.to_numpy(float),
        (matched.measurement_chennai - matched.measurement_hyderabad).to_numpy(float))
    notes.append(f'**Difference in trends (Chennai − Hyderabad):** {fit.slope*10:+.3f} {unit_decade}; exploratory paired annual-difference regression p={fit.pvalue:.4f}.')
    notes.append('**Method:** Temperature is the mean of 12 monthly temperature means per complete year (not weighted by days). '
        'Precipitation is the sum of 12 monthly totals, each computed as monthly mean rate × actual seconds in that calendar month. '
        'A linear regression on 21 annual observations estimates the trend and its conventional 95% confidence interval.')
    notes.append('**Limitations:** MERRA-2 is coarse-grid reanalysis, not direct city-station observations. '
        'Regression p-values do not account for serial autocorrelation; significance is exploratory. '
        'Comparing variables or cities does not establish causation. Check the actual data bounding boxes in the table.')
    figure.update_layout(title=f'NASA MERRA-2 · Annual {variable.lower()} · 2005–2025',
        xaxis_title='Year', yaxis_title=f'Annual mean temperature ({unit})' if variable=='Temperature' else 'Annual precipitation total (mm)',
        template='plotly_white', legend=dict(orientation='h',y=-.28), margin=dict(b=120))
    return figure, pd.DataFrame(rows), '\n\n'.join(notes), ai_rows, float(fit.slope*10), float(fit.pvalue)

with gr.Blocks(title='EarthScope AI | CosmoForge AI') as demo:
    gr.Markdown('# EarthScope AI — Earth System Trend Detective\n### CosmoForge AI · NASA Space Apps Challenge 2026\nExplore NASA MERRA-2 annual temperature and precipitation trends for Chennai and Hyderabad, 2005–2025.')
    variable = gr.Dropdown(choices=['Temperature','Precipitation'],value='Temperature',label='Earth science variable')
    gr.Markdown('**Sources:** NASA Giovanni MERRA-2 `M2TMNXSLV` (`T2M`, Kelvin) and `M2TMNXFLX` (`PRECTOTCORR`, kg/m²/s). Results are computed in Python; no LLM invents statistics.')
    btn = gr.Button('Analyze both regions',variant='primary')
    chart = gr.Plot(label='Annual observations and fitted trends')
    table = gr.Dataframe(label='Trend comparison and spatial provenance')
    explanation = gr.Markdown()
    ai_rows_state = gr.State([])
    diff_slope_state = gr.State(0.0)
    diff_p_state = gr.State(1.0)
    gr.Markdown('### Gemini AI Scientific Analyst\nAI explanations are optional and generated only from the Python-computed statistics. Do not treat them as independent scientific validation.')
    ai_btn = gr.Button('Generate AI explanation')
    ai_output = gr.Markdown('Click **Generate AI explanation** after choosing a variable.')
    analysis_outputs = [chart, table, explanation, ai_rows_state, diff_slope_state, diff_p_state]
    btn.click(compare, inputs=variable, outputs=analysis_outputs)
    variable.change(compare, inputs=variable, outputs=analysis_outputs).then(lambda: 'Variable changed. Generate a new AI explanation for these results.', outputs=ai_output)
    demo.load(lambda: compare('Temperature'), outputs=analysis_outputs)
    ai_btn.click(explain, inputs=[variable, ai_rows_state, diff_slope_state, diff_p_state], outputs=ai_output)

if __name__ == '__main__':
    demo.launch()
