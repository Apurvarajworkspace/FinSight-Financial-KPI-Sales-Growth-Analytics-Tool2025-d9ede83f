# FinSight Command Reference - All Available Modes

## Quick Start

### Run Everything
```bash
python main.py --mode all
```

### Run All New Advanced Features
```bash
python main.py --mode extended
```

## Individual Mode Commands

### Original Analytics Modes (10 modes)
```bash
python main.py --mode demo                 # Standard demo with basic KPIs
python main.py --mode advanced            # Advanced analytics (anomalies, scenarios, cohorts)
python main.py --mode ml_forecast         # ML-based time series forecasting
python main.py --mode segmentation        # Customer segmentation & RFM analysis
python main.py --mode attribution         # Performance attribution analysis
python main.py --mode ratios               # Financial ratios & KPI metrics
python main.py --mode export               # Data export (CSV, JSON, Excel, HTML)
```

### NEW Advanced Analytics Modes (4 modes)
```bash
python main.py --mode predictive          # Predictive Models
  - Customer Lifetime Value (CLV) prediction
  - Churn risk forecasting
  - Revenue prediction ensemble
  - Time series forecasting (ARIMA + Prophet)
  - Anomaly prediction

python main.py --mode basket               # Market Basket Analysis
  - Transaction preparation
  - Apriori frequent itemset mining
  - Association rule generation
  - Cross-sell opportunity identification
  - Sequential pattern discovery

python main.py --mode benchmarking         # Competitive Benchmarking
  - Company vs market metrics comparison
  - Competitive gap analysis
  - Market share analysis & ranking
  - Market opportunity scoring
  - Trend analysis

python main.py --mode portfolio            # Portfolio Optimization
  - BCG matrix analysis (Stars/Cows/Dogs/Questions)
  - Product portfolio recommendations
  - Resource allocation optimization
  - Efficient frontier calculation
```

### Orchestrator Mode (1 mode)
```bash
python main.py --mode extended            # Runs all 4 new advanced modes sequentially
```

### Data Processing Modes (with input file)
```bash
python main.py --mode process --input data.csv
python main.py --mode analyze --input data.csv
python main.py --mode forecast --input data.csv
python main.py --mode report --input data.csv
```

## Output Locations

### Auto-Generated Directories
- `exports/` - CSV, JSON, Excel, HTML outputs
- `reports/` - HTML reports and dashboards

### Generated Files
- `exports/transactions.csv` - Transaction data
- `exports/summary.json` - JSON summary metrics
- `exports/summary_metrics.json` - Updated metrics
- `exports/report.html` - Interactive dashboard
- `exports/report.xlsx` - Excel workbook with multiple sheets
- `reports/demo_report.html` - HTML report

## Mode Descriptions

### Standard Modes (--mode demo)
**Features**: 
- Total revenue & profit margin calculation
- Basic KPI analysis
- Simple trend detection

**Output**: Console metrics and JSON export

### Advanced Modes (--mode advanced)
**Features**:
- Z-score & IQR anomaly detection
- Growth/cost/price elasticity scenarios
- Cohort analysis with retention tracking
- Statistical hypothesis testing
- Risk metrics (VaR, CVaR, Sharpe ratio)

**Output**: Detailed analysis with scenario projections

### ML Forecasting (--mode ml_forecast)
**Features**:
- ARIMA-like forecasting
- Exponential smoothing
- ML regression ensemble methods
- Multi-step forecasts with confidence intervals
- Forecast accuracy metrics

**Output**: Time series predictions with confidence bands

### Segmentation (--mode segmentation)
**Features**:
- RFM scoring (Recency, Frequency, Monetary)
- 8-segment customer classification
- K-means clustering analysis
- Customer Lifetime Value scoring
- Churn prediction

**Output**: Customer segments with actionable classifications

### Attribution (--mode attribution)
**Features**:
- Revenue bridge decomposition
- Volume vs mix effects analysis
- Multi-dimensional contribution analysis
- Performance benchmarking

**Output**: Revenue drivers identified

### Ratios (--mode ratios)
**Features**:
- Profitability ratios (ROA, ROE, net margin)
- Liquidity ratios (current, quick)
- Efficiency ratios (asset turnover, inventory)
- Leverage ratios (debt-to-equity)
- Market ratios (KPI tracking)

**Output**: Comprehensive financial metrics

### Export (--mode export)
**Features**:
- Multi-format export (CSV, JSON, Excel, HTML)
- Batch export capability
- Formatted output with currency/percentage/numbers
- HTML table generation

**Output**: Files in exports/ directory

### Predictive (--mode predictive) ⭐ NEW
**Features**:
- CLV prediction with feature importance
- Churn risk with F1/AUC metrics
- Revenue ensemble (gradient boost + random forest)
- ARIMA & Prophet-style time series
- Anomaly prediction with impact assessment

**Output**: ML predictions with model metrics

### Market Basket (--mode basket) ⭐ NEW
**Features**:
- Apriori frequent itemset discovery
- Association rule generation (confidence/lift)
- Cross-sell recommendations
- Product clustering by association
- Sequential pattern mining

**Output**: Buying patterns and recommendations

### Competitive Benchmarking (--mode benchmarking) ⭐ NEW
**Features**:
- Company vs market metric comparison
- Market positioning analysis
- Competitive gap identification
- Market share ranking
- Opportunity scoring (0-10 scale)

**Output**: Competitive positioning report

### Portfolio Optimization (--mode portfolio) ⭐ NEW
**Features**:
- BCG matrix categorization
- Portfolio recommendations (invest/maintain/harvest/divest)
- Budget-constrained resource allocation
- Efficient frontier with risk/return tradeoff
- ROI optimization

**Output**: Portfolio strategy and optimization results

### Extended (--mode extended) ⭐ NEW
**Runs all 4 new advanced modes sequentially**:
1. Predictive Analytics
2. Market Basket Analysis
3. Competitive Benchmarking
4. Portfolio Optimization

**Output**: Complete advanced analytics suite

## Performance

| Mode | Runtime | Output Size | Typical Use |
|------|---------|-------------|------------|
| demo | <1 sec | 5 KB | Quick validation |
| all | 10-15 sec | 100+ KB | Full analysis |
| extended | 8-12 sec | 80 KB | New features test |
| predictive | 2-3 sec | 20 KB | ML predictions |
| basket | 1-2 sec | 15 KB | Cross-sell analysis |
| benchmarking | 1-2 sec | 10 KB | Market positioning |
| portfolio | 2-3 sec | 25 KB | Portfolio strategy |

## Environment Setup

```bash
# Python version
python --version  # Should be 3.10+

# Check virtual environment
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --mode demo
```

## Troubleshooting

### Unicode Encoding Errors
**Issue**: `UnicodeEncodeError: 'charmap' codec can't encode character`
**Solution**: Already fixed - all special characters replaced with ASCII equivalents

### Import Errors
**Issue**: `ModuleNotFoundError: No module named ...`
**Solution**: 
```bash
pip install -r requirements.txt
python -m pip install --upgrade pip
```

### No Data Generated
**Issue**: `ValueError: Cannot perform reduce with empty sequence`
**Solution**: Data is auto-generated - ensure all 20 modules are present

### File Not Found (exports/reports)
**Issue**: `FileNotFoundError: [Errno 2] No such file or directory`
**Solution**: Directories are auto-created; if issue persists:
```bash
mkdir exports
mkdir reports
```

## Documentation Files

- **README.md** - Project overview
- **00_START_HERE.md** - Entry point with setup
- **QUICK_START.md** - Fast reference
- **RUN_GUIDE.md** - Comprehensive guide (50+ sections)
- **COMMAND_REFERENCE.md** - This file
- **ADVANCED_FEATURES.md** - Feature details
- **COMPLETION_SUMMARY.md** - Full project overview

## Notes

- Sample data generates 365 days × 100 customers × 6 categories
- All demos use randomly generated synthetic data
- No external database required
- All outputs in JSON, CSV, Excel, HTML formats
- Platform runs completely standalone
