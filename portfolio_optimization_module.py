"""
Portfolio Optimization Module - Maximize returns, minimize risk
Product portfolio, investment optimization, resource allocation
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize, LinearConstraint, Bounds


class PortfolioOptimization:
    """Optimize portfolio composition for risk-return balance"""
    
    def __init__(self):
        self.assets = {}
        self.correlations = None
    
    def set_assets(self, assets_dict):
        """Set asset returns and risk profiles"""
        self.assets = assets_dict
        return {
            'assets_added': len(assets_dict),
            'status': 'ready'
        }
    
    def calculate_portfolio_metrics(self, weights, returns, cov_matrix):
        """Calculate portfolio expected return and risk"""
        try:
            portfolio_return = np.sum(weights * returns)
            portfolio_std = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
            
            return {
                'expected_return': portfolio_return,
                'risk_std': portfolio_std,
                'sharpe_ratio': portfolio_return / (portfolio_std + 1e-10)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def min_variance_portfolio(self, returns, cov_matrix):
        """Find minimum variance portfolio"""
        try:
            n = len(returns)
            
            def variance(weights):
                return np.dot(weights, np.dot(cov_matrix, weights))
            
            constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            bounds = tuple((0, 1) for _ in range(n))
            initial_weights = np.array([1/n] * n)
            
            result = minimize(variance, initial_weights, method='SLSQP', 
                            bounds=bounds, constraints=constraints)
            
            optimal_weights = result.x
            metrics = self.calculate_portfolio_metrics(optimal_weights, returns, cov_matrix)
            
            return {
                'optimal_weights': {f'asset_{i}': w for i, w in enumerate(optimal_weights)},
                'expected_return': round(metrics['expected_return'], 4),
                'risk': round(metrics['risk_std'], 4),
                'sharpe_ratio': round(metrics['sharpe_ratio'], 4),
                'status': 'optimized'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def max_sharpe_portfolio(self, returns, cov_matrix, risk_free_rate=0.02):
        """Find maximum Sharpe ratio portfolio"""
        try:
            n = len(returns)
            
            def negative_sharpe(weights):
                ret = np.sum(weights * returns)
                std = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
                sharpe = (ret - risk_free_rate) / (std + 1e-10)
                return -sharpe
            
            constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            bounds = tuple((0, 1) for _ in range(n))
            initial_weights = np.array([1/n] * n)
            
            result = minimize(negative_sharpe, initial_weights, method='SLSQP',
                            bounds=bounds, constraints=constraints)
            
            optimal_weights = result.x
            metrics = self.calculate_portfolio_metrics(optimal_weights, returns, cov_matrix)
            
            return {
                'optimal_weights': {f'asset_{i}': round(w, 4) for i, w in enumerate(optimal_weights)},
                'expected_return': round(metrics['expected_return'], 4),
                'risk': round(metrics['risk_std'], 4),
                'sharpe_ratio': round(metrics['sharpe_ratio'], 4),
                'excess_return': round(metrics['expected_return'] - risk_free_rate, 4),
                'status': 'optimized'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def efficient_frontier(self, returns, cov_matrix, num_portfolios=100):
        """Generate efficient frontier"""
        try:
            n = len(returns)
            results = []
            
            for target_return in np.linspace(np.min(returns), np.max(returns), num_portfolios):
                constraints = [
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                    {'type': 'eq', 'fun': lambda x: np.sum(x * returns) - target_return}
                ]
                
                def variance(weights):
                    return np.dot(weights, np.dot(cov_matrix, weights))
                
                bounds = tuple((0, 1) for _ in range(n))
                initial_weights = np.array([1/n] * n)
                
                result = minimize(variance, initial_weights, method='SLSQP',
                                bounds=bounds, constraints=constraints)
                
                if result.success:
                    std = np.sqrt(result.fun)
                    results.append({
                        'return': target_return,
                        'risk': std,
                        'sharpe_ratio': target_return / std if std != 0 else 0
                    })
            
            return {
                'frontier': results,
                'frontier_length': len(results),
                'min_risk': round(min(r['risk'] for r in results), 4) if results else 0,
                'max_return': round(max(r['return'] for r in results), 4) if results else 0
            }
        except Exception as e:
            return {'error': str(e)}


class ProductPortfolioOptimization:
    """Optimize product portfolio for revenue and margin"""
    
    def __init__(self):
        self.products = {}
    
    def analyze_portfolio(self, df, product_col, revenue_col, margin_col, volume_col):
        """Analyze product portfolio using BCG matrix"""
        try:
            portfolio = df.groupby(product_col).agg({
                revenue_col: 'sum',
                margin_col: 'mean',
                volume_col: 'sum'
            }).reset_index()
            
            total_revenue = portfolio[revenue_col].sum()
            avg_margin = portfolio[margin_col].mean()
            avg_volume = portfolio[volume_col].mean()
            
            # BCG Matrix classification
            portfolio['revenue_pct'] = portfolio[revenue_col] / total_revenue * 100
            portfolio['market_share_proxy'] = portfolio[volume_col] / portfolio[volume_col].sum() * 100
            
            classifications = []
            for idx, row in portfolio.iterrows():
                if row[margin_col] > avg_margin and row[revenue_col] > portfolio[revenue_col].median():
                    classification = 'STAR'
                elif row[margin_col] > avg_margin and row[revenue_col] <= portfolio[revenue_col].median():
                    classification = 'CASH_COW'
                elif row[margin_col] <= avg_margin and row[revenue_col] > portfolio[revenue_col].median():
                    classification = 'QUESTION_MARK'
                else:
                    classification = 'DOG'
                
                classifications.append(classification)
            
            portfolio['classification'] = classifications
            
            # Portfolio summary
            summary = {
                'stars': len(portfolio[portfolio['classification'] == 'STAR']),
                'cash_cows': len(portfolio[portfolio['classification'] == 'CASH_COW']),
                'question_marks': len(portfolio[portfolio['classification'] == 'QUESTION_MARK']),
                'dogs': len(portfolio[portfolio['classification'] == 'DOG']),
                'total_products': len(portfolio)
            }
            
            return {
                'portfolio': portfolio.to_dict('records'),
                'summary': summary,
                'avg_margin': round(avg_margin, 2),
                'portfolio_diversity': len(portfolio),
                'status': 'analyzed'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def portfolio_optimization_recommendation(self, portfolio_df):
        """Recommend portfolio optimization actions"""
        try:
            recommendations = {
                'invest': [],
                'maintain': [],
                'harvest': [],
                'divest': []
            }
            
            for idx, row in portfolio_df.iterrows():
                if row['classification'] == 'STAR':
                    recommendations['invest'].append({
                        'product': row.get('product', f'Product_{idx}'),
                        'reason': 'High growth and profit potential',
                        'action': 'Increase investment and market share'
                    })
                elif row['classification'] == 'CASH_COW':
                    recommendations['maintain'].append({
                        'product': row.get('product', f'Product_{idx}'),
                        'reason': 'Stable revenue and high margin',
                        'action': 'Maintain market share, optimize costs'
                    })
                elif row['classification'] == 'QUESTION_MARK':
                    recommendations['invest'].append({
                        'product': row.get('product', f'Product_{idx}'),
                        'reason': 'High growth, need to improve margin',
                        'action': 'Strategic investment or price optimization'
                    })
                else:  # DOG
                    recommendations['divest'].append({
                        'product': row.get('product', f'Product_{idx}'),
                        'reason': 'Low growth and margin',
                        'action': 'Consider discontinuation or repositioning'
                    })
            
            return {
                'recommendations': recommendations,
                'action_count': sum(len(v) for v in recommendations.values()),
                'portfolio_health': 'healthy' if len(recommendations['invest']) + len(recommendations['maintain']) > len(recommendations['divest']) else 'needs_attention'
            }
        except Exception as e:
            return {'error': str(e)}


class ResourceAllocationOptimizer:
    """Optimize resource allocation across projects/products"""
    
    def __init__(self):
        self.resources = {}
        self.projects = {}
    
    def optimize_resource_allocation(self, budget, projects, resource_requirements):
        """Allocate limited budget across projects for max ROI"""
        try:
            allocations = {}
            remaining_budget = budget
            
            # Sort projects by ROI
            sorted_projects = sorted(projects.items(), 
                                   key=lambda x: x[1]['roi'], 
                                   reverse=True)
            
            for project_name, project_data in sorted_projects:
                required = resource_requirements.get(project_name, 0)
                
                if remaining_budget >= required:
                    allocated = required
                    remaining_budget -= allocated
                else:
                    allocated = remaining_budget if remaining_budget > 0 else 0
                    remaining_budget = 0
                
                allocations[project_name] = {
                    'allocated': allocated,
                    'requested': required,
                    'status': 'fully_funded' if allocated >= required else 'partially_funded' if allocated > 0 else 'not_funded',
                    'expected_roi': (allocated * project_data['roi']) if allocated > 0 else 0,
                    'priority': project_data.get('priority', 5)
                }
            
            # Calculate portfolio ROI
            total_expected_roi = sum(a['expected_roi'] for a in allocations.values())
            
            return {
                'allocations': allocations,
                'total_allocated': budget - remaining_budget,
                'unallocated_budget': remaining_budget,
                'expected_total_roi': round(total_expected_roi, 2),
                'efficiency': round((budget - remaining_budget) / budget * 100, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def constraint_optimization(self, projects, constraints):
        """Optimize allocation with multiple constraints"""
        try:
            results = {
                'feasible_solutions': [],
                'optimal_solution': None,
                'constraints_satisfied': 0
            }
            
            for project_name, project_data in projects.items():
                feasible = True
                
                # Check each constraint
                for constraint_name, constraint_value in constraints.items():
                    if constraint_name == 'budget':
                        if project_data.get('cost', 0) > constraint_value:
                            feasible = False
                    elif constraint_name == 'timeline':
                        if project_data.get('duration', 0) > constraint_value:
                            feasible = False
                    elif constraint_name == 'team_size':
                        if project_data.get('team_required', 0) > constraint_value:
                            feasible = False
                
                if feasible:
                    results['feasible_solutions'].append({
                        'project': project_name,
                        'roi': project_data.get('roi', 0),
                        'cost': project_data.get('cost', 0),
                        'benefit': project_data.get('benefit', 0)
                    })
            
            # Find optimal
            if results['feasible_solutions']:
                results['optimal_solution'] = max(
                    results['feasible_solutions'],
                    key=lambda x: x.get('roi', 0)
                )
                results['constraints_satisfied'] = len(results['feasible_solutions'])
            
            return results
        except Exception as e:
            return {'error': str(e)}
