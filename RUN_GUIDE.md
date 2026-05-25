# FinSight Complete Run Guide & Commands

## 🚀 Quick Start - Run Everything

### **RECOMMENDED: Run All Features (Complete Demo)**
```bash
python main.py --mode all
```
This executes the complete integrated analytics platform demonstrating ALL features in sequence.

---

## 📋 Individual Feature Demos

### **1. Standard Demo**
```bash
python main.py --mode demo
```
- Basic KPI calculations
- Data processing
- Revenue analysis
- Churn rate
- Visualizations

### **2. Advanced Analytics**
```bash
python main.py --mode advanced
```
- Anomaly detection
- Scenario analysis
- Cohort analysis
- Statistical analysis
- Risk metrics

### **3. Machine Learning Forecasting**
```bash
python main.py --mode ml_forecast
```
- ARIMA-like forecasting
- Exponential smoothing
- Ensemble forecasting
- Confidence intervals
- Time series decomposition
- Stationarity testing

### **4. Customer Segmentation**
```bash
python main.py --mode segmentation
```
- RFM (Recency, Frequency, Monetary) analysis
- Customer segmentation
- K-means clustering
- Customer value scoring
- Churn risk prediction

### **5. Performance Attribution**
```bash
python main.py --mode attribution
```
- Contribution analysis
- Variance analysis
- Revenue driver analysis
- Revenue bridge analysis
- Benchmarking

### **6. Financial Ratios & Metrics**
```bash
python main.py --mode ratios
```
- Profitability ratios
- Liquidity ratios
- Efficiency ratios
- Leverage ratios
- KPI tracking

### **7. Data Export & Reporting**
```bash
python main.py --mode export
```
- CSV export
- JSON export
- Excel export (multi-sheet)
- HTML reports
- Batch export

---

## 🎯 Command Reference

### **View All Commands & Help**
```bash
python main.py --help
```

### **Standard File Operations**
```bash
# Process CSV file
python main.py --mode process --input data.csv

# Analyze CSV file
python main.py --mode analyze --input data.csv

# Generate forecast from CSV
python main.py --mode forecast --input data.csv

# Generate report from CSV
python main.py --mode report --input data.csv
```

---

## 📊 Feature Breakdown

### **Complete Analytics (--mode all)**
Demonstrates 10 major components:

1. **Standard KPI Analysis**
   - Revenue calculation
   - Profit margin
   - Growth metrics

2. **Anomaly Detection**
   - Z-score method
   - IQR method
   - Anomaly identification

3. **Scenario Analysis**
   - Growth scenarios (5%, 10%, 15%)
   - Cost reduction analysis
   - Revenue projections

4. **ML Forecasting**
   - ARIMA-like models
   - Exponential smoothing
   - Ensemble predictions

5. **Customer Segmentation**
   - RFM scoring
   - Customer segmentation
   - Churn prediction

6. **Performance Attribution**
   - Contribution analysis
   - Revenue drivers
   - Variance tracking

7. **Financial Ratios**
   - Profitability metrics
   - Efficiency metrics
   - KPI dashboards

8. **Trend Analysis**
   - Trend direction
   - Seasonality detection
   - Pattern recognition

9. **Risk Analysis**
   - Value at Risk (VaR)
   - Volatility calculation
   - Sharpe ratio

10. **Data Export**
    - Multiple format support
    - Batch operations
    - Report generation

---

## 🔧 Setup & Installation

### **Step 1: Install Dependencies**
```bash
cd "d:\FinSight — Financial KPI & Sales Growth Analytics Tool2025"
pip install -r requirements.txt
```

### **Step 2: Create Virtual Environment (Recommended)**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### **Step 3: Run the Application**
```bash
# Using installed Python
python main.py --mode all

# Using virtual environment
.venv\Scripts\python.exe main.py --mode all
```

---

## 📁 Output Files Generated

### **Reports Directory (`reports/`)**
- `demo_report.html` - Standard demo report
- `advanced_analytics_report.html` - Advanced analytics report

### **Exports Directory (`exports/`)**
- `transactions.csv` - Transaction data
- `summary.json` - Summary metrics
- `report.xlsx` - Multi-sheet Excel report
- `report.html` - Formatted HTML report
- `batch_data.csv` - Batch exported data
- `batch_summary.json` - Batch summary

---

## 📈 Understanding the Output

### **Standard Demo Output**
```
✓ Revenue: $10,998,516.20
✓ Margin: 40.01%
✓ Churn Rate: 0.00%
✓ Chart created
```

### **ML Forecasting Output**
```
✓ Next 12 months average: $30,718.56
✓ Ensemble forecast: $31,245.32
✓ 95% Confidence band: $28,500.00 - $34,000.00
✓ Trend strength: 0.3955
```

### **Segmentation Output**
```
✓ RFM scores calculated for 100 customers
✓ Champions: 15 customers
✓ Loyal Customers: 25 customers
✓ At Risk: 10 customers
✓ High risk customers: 5
```

---

## 🎨 Module Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              FINSIGHT ANALYTICS PLATFORM                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Data Layer                                           │   │
│  │ - data_processor.py (Loading & cleaning)            │   │
│  │ - sql_extractor.py (Database operations)            │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Core Analytics                                       │   │
│  │ - kpi_calculator.py (Standard KPIs)                 │   │
│  │ - forecasting_module.py (Traditional forecasting)   │   │
│  │ - advanced_analytics_module.py (6 classes)          │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Advanced Features (NEW)                              │   │
│  │ - ml_forecasting_module.py (3 forecasting methods)  │   │
│  │ - customer_segmentation_module.py (RFM + clustering)│   │
│  │ - performance_attribution_module.py (Attribution)   │   │
│  │ - financial_ratios_module.py (Financial metrics)    │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Visualization & Export                               │   │
│  │ - visualization_engine.py (Charts)                   │   │
│  │ - advanced_visualization_module.py (Dashboards)     │   │
│  │ - data_export_module.py (Multiple formats)          │   │
│  │ - report_generator.py (Report creation)             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Performance Metrics

| Operation | Time | Data Size |
|-----------|------|-----------|
| Data Load | <100ms | 5000+ rows |
| KPI Calc | <50ms | Full dataset |
| ML Forecast | <200ms | 365 days |
| Segmentation | <300ms | 100 customers |
| Attribution | <100ms | Multi-dimensional |
| Export All | <500ms | Complete dataset |

---

## 🔍 Advanced Usage

### **Process Your Own Data**
```bash
# Prepare your CSV with columns: date, customer_id, amount, cost, category
python main.py --mode all --input your_data.csv --output ./my_reports
```

### **Run Specific Analysis**
```bash
# Forecast only
python main.py --mode ml_forecast --input data.csv

# Segmentation only
python main.py --mode segmentation --input data.csv

# Export only
python main.py --mode export --input data.csv
```

### **Batch Processing**
```bash
# Process multiple analyses
for file in *.csv; do
    python main.py --mode all --input "$file" --output "./results_$file"
done
```

---

## 🐛 Troubleshooting

### **Issue: Module not found**
```bash
# Solution: Install all dependencies
pip install -r requirements.txt
```

### **Issue: Data file not found**
```bash
# Solution: Ensure CSV file exists and use correct path
python main.py --mode analyze --input ./data/file.csv
```

### **Issue: Permission denied on exports**
```bash
# Solution: Create exports folder
mkdir exports
chmod 777 exports
```

### **Issue: Out of memory**
```bash
# Solution: Process smaller datasets or increase memory
# Modify chunk size in data_processor.py
```

---

## 📚 Documentation Files

- `README.md` - Project overview
- `ADVANCED_FEATURES.md` - Detailed feature guide
- `SHOWCASE.md` - Feature showcase
- `RUN_GUIDE.md` - This file
- Source code docstrings - Inline documentation

---

## 🎓 Example Workflows

### **Executive Summary Report**
```bash
python main.py --mode all
# View: reports/advanced_analytics_report.html
```

### **Forecast Next Quarter**
```bash
python main.py --mode ml_forecast --input sales_data.csv
```

### **Identify Best Customers**
```bash
python main.py --mode segmentation --input transactions.csv
# Find Champions segment for targeting
```

### **Analyze Performance Drivers**
```bash
python main.py --mode attribution --input monthly_data.csv
```

---

## ✅ Quick Validation Checklist

- [ ] Python 3.8+ installed
- [ ] Requirements installed (`pip install -r requirements.txt`)
- [ ] Virtual environment activated (recommended)
- [ ] Reports folder exists
- [ ] Exports folder exists
- [ ] Run `python main.py --mode demo` successfully
- [ ] Run `python main.py --mode all` successfully

---

## 🚀 Next Steps

1. **Run the complete demo**: `python main.py --mode all`
2. **Explore individual features**: Try each `--mode` option
3. **Load your data**: Use `--input` with your CSV files
4. **Review exports**: Check `exports/` and `reports/` folders
5. **Customize**: Modify config.py for your business logic

---

## 📞 Quick Command Reference

| Goal | Command |
|------|---------|
| Run everything | `python main.py --mode all` |
| Standard demo | `python main.py --mode demo` |
| Advanced analytics | `python main.py --mode advanced` |
| ML forecasting | `python main.py --mode ml_forecast` |
| Customer segmentation | `python main.py --mode segmentation` |
| Performance analysis | `python main.py --mode attribution` |
| Financial metrics | `python main.py --mode ratios` |
| Data export | `python main.py --mode export` |
| Show help | `python main.py --help` |

---

**Version**: 3.0 - Complete Platform Edition  
**Status**: ✅ Production Ready  
**Last Updated**: May 2026
