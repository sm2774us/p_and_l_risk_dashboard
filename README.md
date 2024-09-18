# p_and_l_risk_dashboard

Creating an open-source project for live calculation of P&L and risk analysis is a powerful tool for portfolio managers. Here's a structured approach to set up this project with GitHub Actions, Python3, Dash for dashboards, NumPy, Pandas, PostgreSQL for database operations, Pytest for unit testing, and Docker/Kubernetes for deployment and isolation.

### Project Structure

```bash
├── p_and_l_risk_dashboard
│   ├── app
│   │   ├── __init__.py
│   │   ├── data_fetch.py        # Functions for data fetching and processing
│   │   ├── risk_calculator.py   # Functions to calculate risk and P&L
│   │   ├── dashboard.py         # Dash app for the portfolio manager's interface
│   ├── notebooks
│   │   └── portfolio_analysis.ipynb  # Jupyter notebook for portfolio analysis
│   ├── tests
│   │   ├── test_data_fetch.py   # Unit tests for data fetching
│   │   ├── test_risk_calculator.py   # Unit tests for P&L and risk calculations
│   ├── docker
│   │   ├── Dockerfile           # Dockerfile for containerization
│   │   └── docker-compose.yml   # Docker Compose for local environment
│   ├── k8s
│   │   ├── deployment.yaml      # Kubernetes deployment configuration
│   │   └── service.yaml         # Kubernetes service for the Dash app
│   ├── .github
│   │   └── workflows
│   │       └── python-app.yml   # GitHub Actions CI/CD workflow
│   ├── requirements.txt         # Required dependencies
│   ├── README.md                # Project description
│   └── setup.py                 # Package information
```

### Key Components

1. **Data Handling (PostgreSQL with Pandas)**:
    - Fetch data from a PostgreSQL database using Pandas to read and analyze live market data.
    - Calculate live risk metrics (P&L, VaR, portfolio exposure) based on asset categories: interest rate swaps, fixed income futures, interest rate options, and foreign exchange.

2. **Risk & P&L Calculation (Python/Numpy)**:
    - Implement a core module to calculate P&L and risk.
    - Use NumPy and Pandas for efficient numerical operations and data transformations.

3. **Dash for Visualization**:
    - Build an interactive dashboard using Dash to display real-time portfolio performance, risk metrics, and P&L.
    - The dashboard will show live updates from the Postgres database.

4. **Jupyter Notebook**:
    - Create a notebook (`notebooks/portfolio_analysis.ipynb`) for researchers to analyze historical data and perform simulations on the portfolio.

5. **Docker & Kubernetes**:
    - Use a `Dockerfile` to containerize the application for reproducibility and portability.
    - `docker-compose.yml` to orchestrate local development and testing.
    - Kubernetes configuration (`k8s/`) to deploy the Dash application on the cloud with scalability and isolation.

6. **GitHub Actions for CI/CD**:
    - Automate tests and deployment pipelines using GitHub Actions.
    - `python-app.yml` for continuous integration—ensures code quality and automated testing with Pytest.
    - Use actions for building and pushing Docker images, running unit tests, and deploying to Kubernetes.

### Sample Code

#### 1. **Data Fetching (`app/data_fetch.py`)**:

```python
import pandas as pd
import psycopg2

def fetch_market_data():
    conn = psycopg2.connect(
        dbname="portfolio_db", user="user", password="password", host="localhost", port="5432"
    )
    query = "SELECT * FROM market_data;"
    data = pd.read_sql(query, conn)
    conn.close()
    return data
```

#### 2. **Risk Calculation (`app/risk_calculator.py`)**:

```python
import numpy as np
import pandas as pd

def calculate_pnl(data: pd.DataFrame):
    # Assume data contains 'asset_value' and 'quantity' columns
    data['pnl'] = data['asset_value'] * data['quantity']
    total_pnl = np.sum(data['pnl'])
    return total_pnl

def calculate_risk_exposure(data: pd.DataFrame):
    # Simple VaR calculation using historical method (for demonstration)
    returns = data['asset_value'].pct_change().dropna()
    var = np.percentile(returns, 5) * np.sqrt(len(returns))
    return var
```

#### 3. **Dashboard (`app/dashboard.py`)**:

```python
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
```

#### 4. **Dockerfile**:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app/dashboard.py"]
```

#### 5. **Kubernetes Deployment (`k8s/deployment.yaml`)**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: p-and-l-dashboard
spec:
  replicas: 2
  selector:
    matchLabels:
      app: p-and-l-dashboard
  template:
    metadata:
      labels:
        app: p-and-l-dashboard
    spec:
      containers:
      - name: p-and-l-dashboard
        image: your-dockerhub-username/p-and-l-dashboard:latest
        ports:
        - containerPort: 8050
```

#### 6. **GitHub Actions (`.github/workflows/python-app.yml`)**:

```yaml
name: Python application

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: pytest

  docker-build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2
    - name: Build Docker image
      run: |
        docker build -t your-dockerhub-username/p-and-l-dashboard .
        docker push your-dockerhub-username/p-and-l-dashboard
```

### Final Thoughts

- **Notebook**: The notebook (`notebooks/portfolio_analysis.ipynb`) will include code to analyze historical portfolio data, plot P&L and risk over time, and explore different portfolio scenarios using Python and Dash.
- **Deployment**: Use Docker and Kubernetes for consistent environments, scaling the application and handling live updates.
- **GitHub Actions**: Automate testing and deployment, ensuring the project maintains quality standards and is easy to contribute to.

This setup provides a complete open-source project for P&L and risk analysis. You can customize and expand it as needed to handle more sophisticated calculations or new asset categories.

Here’s an example of a Jupyter notebook, `portfolio_analysis.ipynb`, that can be used by researchers and portfolio managers to analyze portfolio performance and risk over time. This notebook integrates with the core modules of the project, allowing users to interactively analyze historical data and run simulations.

### `portfolio_analysis.ipynb`

```python
# Portfolio Analysis and P&L / Risk Calculations

# Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from app.data_fetch import fetch_market_data
from app.risk_calculator import calculate_pnl, calculate_risk_exposure

# Fetch data from PostgreSQL
# Assuming fetch_market_data is fetching live data for analysis
market_data = fetch_market_data()

# Display the first few rows of data to understand its structure
market_data.head()

# Plot the asset value trend over time
plt.figure(figsize=(10, 6))
plt.plot(market_data['timestamp'], market_data['asset_value'], label='Asset Value')
plt.title('Asset Value Trend Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Asset Value')
plt.grid(True)
plt.legend()
plt.show()

# P&L Calculation for the current portfolio
pnl = calculate_pnl(market_data)
print(f"Total Portfolio P&L: {pnl}")

# Risk Exposure (VaR calculation)
risk = calculate_risk_exposure(market_data)
print(f"Portfolio VaR (Value at Risk): {risk}")

# Simulating P&L for different portfolio weights
# Assume we simulate weights of 25%, 50%, and 75% on each asset category
weights = [0.25, 0.50, 0.75]
simulated_pnls = []

for weight in weights:
    # Simulate adjusted P&L based on the weightage
    adjusted_data = market_data.copy()
    adjusted_data['pnl'] = adjusted_data['pnl'] * weight
    simulated_pnls.append(np.sum(adjusted_data['pnl']))

# Plotting P&L simulations for different weightings
plt.figure(figsize=(10, 6))
plt.bar(weights, simulated_pnls, color=['blue', 'green', 'orange'])
plt.title('Simulated P&L for Different Portfolio Weights')
plt.xlabel('Portfolio Weight')
plt.ylabel('P&L')
plt.grid(True)
plt.show()

# Simulate historical VaR for different time horizons (e.g., 1 week, 1 month, 3 months)
time_horizons = ['1W', '1M', '3M']
var_simulations = []

for horizon in time_horizons:
    # Resample data to the given time horizon and calculate VaR
    resampled_data = market_data.resample(horizon, on='timestamp').last()
    var_simulation = calculate_risk_exposure(resampled_data)
    var_simulations.append(var_simulation)

# Plotting VaR simulations for different time horizons
plt.figure(figsize=(10, 6))
plt.bar(time_horizons, var_simulations, color=['blue', 'green', 'red'])
plt.title('Simulated VaR for Different Time Horizons')
plt.xlabel('Time Horizon')
plt.ylabel('VaR')
plt.grid(True)
plt.show()

# Conclusion and Interpretation
print("Analysis Summary:")
print(f"Total P&L: {pnl}")
print(f"VaR (Value at Risk) for current data: {risk}")
print(f"Simulated P&L for different portfolio weights: {simulated_pnls}")
print(f"Simulated VaR for different time horizons: {var_simulations}")
```

### Key Features of the Notebook:
1. **Data Fetching**: Pulls live or historical data from the PostgreSQL database.
2. **P&L and Risk Calculations**: Performs live calculations of portfolio P&L and risk exposure (Value at Risk - VaR).
3. **Visualization**: 
   - Asset value trend over time.
   - P&L simulations for different portfolio weights.
   - VaR simulations over different time horizons.
4. **Interactive Exploration**: Allows portfolio managers and researchers to experiment with different portfolio weights and time horizons for risk analysis.
5. **Conclusion**: Provides a summary of the portfolio's current state based on real-time or simulated data.

### How to Run:
1. Install the necessary Python libraries (`pandas`, `matplotlib`, etc.).
2. Ensure the PostgreSQL database is accessible and that the `fetch_market_data()` function is correctly configured.
3. Run the notebook cell by cell to analyze live data, simulate portfolio performance, and visualize the results.

---

This notebook can be extended to include additional analyses, such as stress testing, scenario analysis, or Monte Carlo simulations, depending on the research and portfolio needs.