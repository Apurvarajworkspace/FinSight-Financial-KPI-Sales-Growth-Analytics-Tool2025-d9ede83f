"""
Main Application Entry Point
Financial KPI Analytics Tool
"""

import pandas as pd
import numpy as np
from data_processor import DataProcessor
from kpi_calculator import KPICalculator
from sql_extractor import SQLExtractor
from forecasting_module import ForecastingModule
from report_generator import ReportGenerator
from visualization_engine import VisualizationEngine
from advanced_analytics_module import (AnomalyDetector, ScenarioAnalyzer, 
                                       CohortAnalyzer, StatisticalAnalyzer, 
                                       RiskAnalyzer, TrendAnalyzer)
from advanced_visualization_module import DashboardBuilder, AlertManager, ReportComposer
from ml_forecasting_module import MLForecaster, TimeSeriesAnalyzer
from customer_segmentation_module import RFMAnalyzer, CustomerClusterer, CustomerValueScorer
from performance_attribution_module import PerformanceAttributor, VarianceExplainer, PerformanceBenchmarking
from financial_ratios_module import FinancialRatios, MetricsAnalyzer, KPITracker
from data_export_module import DataExporter, BatchExporter, ReportFormatter
import argparse
import sys
from datetime import datetime, timedelta


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Financial KPI Analytics Tool')
    parser.add_argument('--mode', choices=['process', 'analyze', 'forecast', 'report', 'demo', 'advanced', 
                                          'ml_forecast', 'segmentation', 'attribution', 'ratios', 'export', 'all'],
                       default='demo', help='Operation mode')
    parser.add_argument('--input', type=str, help='Input CSV file path')
    parser.add_argument('--output', type=str, help='Output directory')
    
    args = parser.parse_args()
    
    if args.mode == 'demo':
        run_demo()
    elif args.mode == 'advanced':
        run_advanced_demo()
    elif args.mode == 'ml_forecast':
        run_ml_forecast_demo()
    elif args.mode == 'segmentation':
        run_segmentation_demo()
    elif args.mode == 'attribution':
        run_attribution_demo()
    elif args.mode == 'ratios':
        run_ratios_demo()
    elif args.mode == 'export':
        run_export_demo()
    elif args.mode == 'all':
        run_complete_analytics()
    elif args.mode == 'process':
        if not args.input:
            print("Error: --input required for process mode")
            sys.exit(1)
        process_data(args.input)
    elif args.mode == 'analyze':
        if not args.input:
            print("Error: --input required for analyze mode")
            sys.exit(1)
        analyze_data(args.input)
    elif args.mode == 'forecast':
        if not args.input:
            print("Error: --input required for forecast mode")
            sys.exit(1)
        forecast_data(args.input)
    elif args.mode == 'report':
        if not args.input:
            print("Error: --input required for report mode")
            sys.exit(1)
        generate_report(args.input)


def run_demo():
    """Run demonstration with sample data"""
    print("=" * 60)
    print("Financial KPI Analytics Tool - Demo Mode")
    print("=" * 60)
    
    # Create sample data
    print("\n1. Creating sample financial data...")
    sample_data = create_sample_data()
    print(f"   Created {len(sample_data)} sample transactions")
    
    # Initialize modules
    data_processor = DataProcessor()
    kpi_calculator = KPICalculator()
    forecasting = ForecastingModule()
    viz_engine = VisualizationEngine()
    
    # Process data
    print("\n2. Processing data...")
    df_processed = data_processor.handle_missing_values(sample_data)
    df_processed = data_processor.remove_duplicates(df_processed)
    print(f"   Processed data: {len(df_processed)} records")
    
    # Calculate KPIs
    print("\n3. Calculating KPIs...")
    
    # Revenue metrics
    total_revenue = kpi_calculator.calculate_total_revenue(df_processed)
    print(f"   Total Revenue: ${total_revenue:,.2f}")
    
    # Profit margins
    df_with_margins = kpi_calculator.calculate_profit_margin(df_processed)
    avg_margin = df_with_margins['profit_margin'].mean()
    print(f"   Average Profit Margin: {avg_margin*100:.2f}%")
    
    # Revenue growth
    growth_df = kpi_calculator.calculate_revenue_growth(df_processed, period_type='month')
    print(f"   Revenue growth calculated for {len(growth_df)} periods")
    
    # Churn rate
    try:
        churn_metrics = kpi_calculator.calculate_churn_rate(df_processed)
        print(f"   Customer Churn Rate: {churn_metrics['churn_rate']:.2f}%")
    except Exception as e:
        print(f"   Churn calculation skipped: {str(e)}")
    
    # Forecasting
    print("\n4. Running forecasting models...")
    
    # CAGR
    try:
        cagr = forecasting.calculate_cagr(100000, 150000, 3)
        print(f"   Sample CAGR (3 years): {cagr:.2f}%")
    except Exception as e:
        print(f"   CAGR calculation error: {str(e)}")
    
    # Exponential smoothing
    historical_sales = df_processed.groupby('date')['revenue'].sum().tolist()[:10]
    if len(historical_sales) >= 3:
        forecast_result = forecasting.exponential_smoothing_forecast(historical_sales, forecast_periods=3)
        print(f"   Sales forecast (next 3 periods): {[f'{x:.2f}' for x in forecast_result['forecasts']]}")
    
    # CLV
    try:
        clv_df = forecasting.calculate_customer_lifetime_value(df_processed)
        avg_clv = clv_df['clv'].mean()
        print(f"   Average Customer Lifetime Value: ${avg_clv:,.2f}")
    except Exception as e:
        print(f"   CLV calculation skipped: {str(e)}")
    
    # Visualizations
    print("\n5. Creating visualizations...")
    
    # Revenue trend chart
    daily_revenue = df_processed.groupby('date')['revenue'].sum().reset_index()
    fig1 = viz_engine.create_line_chart(
        daily_revenue, 'date', 'revenue',
        title="Daily Revenue Trend",
        y_label="Revenue ($)"
    )
    
    # Category performance
    category_revenue = df_processed.groupby('product_category')['revenue'].sum().reset_index()
    category_revenue = category_revenue.sort_values('revenue', ascending=False).head(10)
    fig2 = viz_engine.create_bar_chart(
        category_revenue, 'product_category', 'revenue',
        title="Top 10 Product Categories by Revenue",
        y_label="Revenue ($)"
    )
    
    # Save visualizations
    report_path = viz_engine.embed_in_html(
        [fig1, fig2],
        'reports/demo_report.html',
        title="Financial KPI Analytics - Demo Report"
    )
    print(f"   Report saved to: {report_path}")
    
    # Segment analysis
    print("\n6. Analyzing segments...")
    segment_data = df_processed.groupby('region').agg({
        'revenue': 'sum',
        'cost': 'sum'
    }).reset_index()
    segment_data['profit_margin'] = (segment_data['revenue'] - segment_data['cost']) / segment_data['revenue']
    segment_data['growth_rate'] = 5.0  # Placeholder
    
    if len(segment_data) >= 3:
        segments = kpi_calculator.identify_segments(
            segment_data,
            metrics=['revenue', 'profit_margin'],
            segment_column='region'
        )
        
        high_perf = segments[segments['performance_classification'] == 'High-Performing']
        under_perf = segments[segments['performance_classification'] == 'Underperforming']
        
        print(f"   High-performing segments: {len(high_perf)}")
        print(f"   Underperforming segments: {len(under_perf)}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


def create_sample_data():
    """Create sample financial data for demonstration"""
    import numpy as np
    from datetime import datetime, timedelta
    
    np.random.seed(42)
    
    # Generate dates
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    # Generate sample transactions
    data = []
    customer_ids = [f'CUST{i:04d}' for i in range(1, 101)]
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home', 'Sports']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    for date in dates:
        num_transactions = np.random.randint(5, 20)
        for _ in range(num_transactions):
            revenue = np.random.uniform(50, 5000)
            cost = revenue * np.random.uniform(0.4, 0.8)
            
            data.append({
                'date': date,
                'customer_id': np.random.choice(customer_ids),
                'revenue': round(revenue, 2),
                'cost': round(cost, 2),
                'amount': round(revenue, 2),
                'product_category': np.random.choice(categories),
                'region': np.random.choice(regions)
            })
    
    return pd.DataFrame(data)


def process_data(input_file):
    """Process CSV data"""
    print(f"Processing data from: {input_file}")
    processor = DataProcessor()
    df = processor.process_csv(input_file)
    print(f"Processed {len(df)} records")
    return df


def analyze_data(input_file):
    """Analyze financial data"""
    print(f"Analyzing data from: {input_file}")
    processor = DataProcessor()
    df = processor.load_csv(input_file)
    
    calculator = KPICalculator()
    total_revenue = calculator.calculate_total_revenue(df)
    print(f"Total Revenue: ${total_revenue:,.2f}")


def forecast_data(input_file):
    """Generate forecasts"""
    print(f"Forecasting from: {input_file}")
    processor = DataProcessor()
    df = processor.load_csv(input_file)
    
    forecasting = ForecastingModule()
    # Add forecasting logic here


def generate_report(input_file):
    """Generate financial report"""
    print(f"Generating report from: {input_file}")
    processor = DataProcessor()
    df = processor.load_csv(input_file)
    
    report_gen = ReportGenerator()
    result = report_gen.generate_weekly_report(df)
    print(f"Report status: {result['status']}")
    if result['status'] == 'success':
        print(f"Report saved to: {result['report_path']}")


def run_advanced_demo():
    """Run advanced analytics demonstration"""
    print("=" * 60)
    print("Advanced Analytics Demo - Financial KPI Tool")
    print("=" * 60)
    
    # Create sample data
    print("\n1. Creating sample financial data...")
    sample_data = create_sample_data()
    print(f"   Created {len(sample_data)} transactions")
    
    df = pd.DataFrame(sample_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # ===== ANOMALY DETECTION =====
    print("\n2. Detecting anomalies in revenue...")
    detector = AnomalyDetector(zscore_threshold=2.5)
    revenue_series = df.groupby('date')['revenue'].sum()
    
    zscore_anomalies = detector.detect_zscore_anomalies(revenue_series, window=15)
    print(f"   Z-Score Method: {zscore_anomalies['anomalies']} anomalies detected")
    
    iqr_anomalies = detector.detect_iqr_anomalies(revenue_series)
    print(f"   IQR Method: {iqr_anomalies['anomalies']} anomalies detected")
    print(f"   Normal range: ${iqr_anomalies['lower_bound']:,.2f} - ${iqr_anomalies['upper_bound']:,.2f}")
    
    # ===== SCENARIO ANALYSIS =====
    print("\n3. Running scenario analysis...")
    scenario_analyzer = ScenarioAnalyzer()
    
    # Growth scenarios
    current_revenue = df['revenue'].sum()
    growth_scenarios = scenario_analyzer.growth_scenario(current_revenue, [5.0, 10.0, 15.0], periods=12)
    print("   Revenue Projections (12 months):")
    for scenario, projections in growth_scenarios.items():
        print(f"      {scenario}: ${projections[-1]:,.2f}")
    
    # Cost reduction scenarios
    current_cost = df['cost'].sum()
    cost_scenarios = scenario_analyzer.cost_reduction_scenario(current_revenue, current_cost, [10.0, 20.0, 30.0])
    print("   Cost Reduction Impact:")
    for scenario, metrics in cost_scenarios.items():
        print(f"      {scenario}: Profit improvement: ${metrics['profit_improvement']:,.2f}")
    
    # ===== COHORT ANALYSIS =====
    print("\n4. Performing cohort analysis...")
    cohort_analyzer = CohortAnalyzer()
    cohort_pivot, cohort_sizes = cohort_analyzer.create_cohorts(df, 'customer_id', 'date', 'revenue', 'M')
    print(f"   Identified {len(cohort_pivot)} customer cohorts")
    print(f"   Cohort sizes: {cohort_sizes['cohort_size'].tolist()}")
    
    retention_data = cohort_analyzer.calculate_cohort_retention(df, 'customer_id', 'date', 'M')
    avg_retention = retention_data['retention_rate'].mean()
    print(f"   Average customer retention rate: {avg_retention:.2f}%")
    
    # ===== STATISTICAL ANALYSIS =====
    print("\n5. Performing statistical analysis...")
    stat_analyzer = StatisticalAnalyzer()
    
    # Distribution analysis
    revenue_dist = stat_analyzer.distribution_analysis(df['revenue'])
    print(f"   Revenue Distribution:")
    print(f"      Mean: ${revenue_dist['mean']:,.2f}")
    print(f"      Std Dev: ${revenue_dist['std_dev']:,.2f}")
    print(f"      Skewness: {revenue_dist['skewness']:.4f}")
    print(f"      Normal Distribution: {'Yes' if revenue_dist['is_normal'] else 'No'}")
    
    # Correlation analysis
    numeric_cols = df[['revenue', 'cost']].select_dtypes(include=['number']).columns
    correlation = stat_analyzer.correlation_analysis(df, list(numeric_cols))
    print(f"   Revenue-Cost Correlation: {correlation.loc['revenue', 'cost']:.4f}")
    
    # ===== RISK ANALYSIS =====
    print("\n6. Analyzing financial risk...")
    risk_analyzer = RiskAnalyzer(confidence_level=0.95)
    
    # Calculate daily returns
    daily_revenue = df.groupby('date')['revenue'].sum()
    daily_returns = daily_revenue.pct_change().dropna()
    
    var_metrics = risk_analyzer.calculate_value_at_risk(daily_returns)
    print(f"   Value at Risk (95%): {var_metrics['var']:.4f}")
    print(f"   Conditional VaR: {var_metrics['conditional_var']:.4f}")
    
    volatility = risk_analyzer.calculate_volatility(daily_returns)
    print(f"   Annual Volatility: {volatility['annual_volatility']:.4f} ({volatility['annual_volatility']*100:.2f}%)")
    
    sharpe_ratio = risk_analyzer.calculate_sharpe_ratio(daily_returns)
    print(f"   Sharpe Ratio: {sharpe_ratio:.4f}")
    
    # ===== TREND ANALYSIS =====
    print("\n7. Analyzing trends and seasonality...")
    trend_analyzer = TrendAnalyzer()
    
    trend = trend_analyzer.detect_trend(revenue_series, window=20)
    print(f"   Trend Direction: {trend['trend'].upper()}")
    print(f"   Trend Strength: {trend['strength']:.4f}")
    
    seasonality = trend_analyzer.detect_seasonality(revenue_series, periods=12)
    print(f"   Seasonality Detected: {'Yes' if seasonality['has_seasonality'] else 'No'}")
    if seasonality['strongest_lag']:
        print(f"   Strongest Lag: {seasonality['strongest_lag']['lag']} periods")
    
    # ===== CREATE ADVANCED DASHBOARD =====
    print("\n8. Creating advanced visualizations...")
    dashboard_builder = DashboardBuilder()
    alert_manager = AlertManager()
    
    # KPI Dashboard
    kpi_data = {
        'Total Revenue': current_revenue,
        'Total Cost': current_cost,
        'Profit Margin %': ((current_revenue - current_cost) / current_revenue * 100),
        'Avg Transaction': df['revenue'].mean()
    }
    
    previous_kpi = {
        'Total Revenue': current_revenue * 0.95,
        'Total Cost': current_cost * 0.92,
        'Profit Margin %': ((current_revenue * 0.95 - current_cost * 0.92) / (current_revenue * 0.95) * 100),
        'Avg Transaction': df['revenue'].mean() * 0.93
    }
    
    # Create alerts
    alert_manager.create_threshold_alert('Profit Margin', kpi_data['Profit Margin %'], 30.0, 'below', 'warning')
    alert_manager.create_anomaly_alert('Revenue Anomalies', zscore_anomalies['anomalies'], 'info')
    
    alerts = alert_manager.get_active_alerts().to_dict('records') if not alert_manager.get_active_alerts().empty else []
    
    # Build report
    figures = []
    kpi_fig = dashboard_builder.create_kpi_dashboard(kpi_data, previous_kpi, "Financial KPI Summary")
    figures.append(kpi_fig)
    
    # Waterfall chart for revenue components
    waterfall_fig = dashboard_builder.create_waterfall_chart(
        ['Base Revenue', 'Growth', 'Final Revenue'],
        [current_revenue * 0.8, current_revenue * 0.2, current_revenue],
        "Revenue Waterfall Analysis"
    )
    figures.append(waterfall_fig)
    
    # Correlation heatmap
    heatmap_fig = dashboard_builder.create_heatmap(df[['revenue', 'cost']], "Metric Correlations")
    figures.append(heatmap_fig)
    
    # Compose and save report
    analysis_summary = {
        'Total Anomalies': zscore_anomalies['anomalies'],
        'Cohorts Identified': len(cohort_pivot),
        'Avg Retention': f"{avg_retention:.1f}%",
        'Annual Volatility': f"{volatility['annual_volatility']*100:.2f}%",
        'Trend': trend['trend'].title()
    }
    
    report_composer = ReportComposer()
    report_path = report_composer.create_html_report(
        figures, alerts, analysis_summary,
        "reports/advanced_analytics_report.html"
    )
    print(f"   Advanced report saved to: {report_path}")
    
    print("\n" + "=" * 60)
    print("Advanced Analytics Demo Completed Successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
