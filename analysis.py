import io
import calendar
import numpy as np
import pandas as pd
from scipy import stats


def load_giovanni(path, variable):
    """Read NASA Giovanni monthly CSV, retaining its spatial provenance."""
    with open(path, encoding='utf-8-sig') as f:
        lines = f.read().splitlines()
    metadata = {}
    start = next((i for i, line in enumerate(lines) if line.startswith('time,')), None)
    if start is None:
        raise ValueError(f'No time-series header: {path}')
    for line in lines[:start]:
        if ':,' in line:
            k, v = line.split(':,', 1)
            metadata[k.strip()] = v.strip().strip('"')
    df = pd.read_csv(io.StringIO('\n'.join(lines[start:])), skipinitialspace=True)
    if len(df.columns) != 2:
        raise ValueError('Expected one variable in CSV')
    valcol = df.columns[1]
    expected = 'T2M' if variable == 'Temperature' else 'PRECTOTCORR'
    if expected not in valcol:
        raise ValueError(f'Expected {expected}, got {valcol}')
    df['time'] = pd.to_datetime(df.iloc[:, 0], errors='coerce')
    df['value'] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
    fill = metadata.get(f'Fill Value ({valcol})')
    if fill:
        df.loc[np.isclose(df['value'], float(fill)), 'value'] = np.nan
    df = df.dropna(subset=['time', 'value']).sort_values('time').copy()
    if variable == 'Temperature':
        df['measurement'] = df['value'] - 273.15
    else:
        # MERRA-2 PRECTOTCORR: kg m^-2 s^-1 = mm/s of liquid water equivalent.
        # Convert each monthly mean rate to its corresponding calendar-month total.
        seconds = df['time'].dt.days_in_month * 86400
        df['measurement'] = df['value'] * seconds
    return df, metadata


def analyze(df, variable):
    annual = df.assign(year=df.time.dt.year).groupby('year', as_index=False).agg(
        measurement=('measurement', 'mean' if variable == 'Temperature' else 'sum'),
        months=('measurement', 'size'))
    annual = annual[annual.months == 12].copy()
    if len(annual) < 5:
        raise ValueError('At least five complete years are needed')
    x = annual.year.to_numpy(float)
    y = annual.measurement.to_numpy(float)
    reg = stats.linregress(x, y)
    tcrit = stats.t.ppf(.975, len(x)-2)
    annual['fitted'] = reg.intercept + reg.slope*x
    return annual, dict(n_years=len(x), slope_decade=reg.slope*10,
        ci_low=(reg.slope-tcrit*reg.stderr)*10,
        ci_high=(reg.slope+tcrit*reg.stderr)*10,
        p_value=reg.pvalue, significant=bool(reg.pvalue < .05),
        kendall_p=stats.kendalltau(x,y).pvalue)
