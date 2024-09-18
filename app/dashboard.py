import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from app.data_fetch import fetch_market_data
from app.risk_calculator import calculate_pnl, calculate_risk_exposure

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Portfolio Manager Dashboard"),
    dcc.Graph(id='live-pnl'),
    dcc.Graph(id='live-risk'),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)  # Update every 5 seconds
])

@app.callback(
    Output('live-pnl', 'figure'),
    Output('live-risk', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_metrics(n):
    data = fetch_market_data()
    pnl = calculate_pnl(data)
    risk = calculate_risk_exposure(data)
    
    pnl_fig = {
        'data': [{'x': data['timestamp'], 'y': pnl, 'type': 'line'}],
        'layout': {'title': 'P&L'}
    }
    
    risk_fig = {
        'data': [{'x': data['timestamp'], 'y': risk, 'type': 'line'}],
        'layout': {'title': 'Risk Exposure'}
    }
    
    return pnl_fig, risk_fig

if __name__ == '__main__':
    app.run_server(debug=True)
