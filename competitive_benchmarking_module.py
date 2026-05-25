"""
Competitive Benchmarking Module - Compare with market standards
Market positioning and competitive analysis
"""

import pandas as pd
import numpy as np


class CompetitiveBenchmarking:
    """Analyze competitive position and market standing"""
    
    def __init__(self):
        self.company_data = {}
        self.market_data = {}
        self.benchmarks = {}
    
    def set_company_metrics(self, metrics_dict):
        """Set company's key metrics"""
        self.company_data = metrics_dict
        return {'status': 'company_metrics_set', 'metrics': len(metrics_dict)}
    
    def set_market_benchmarks(self, benchmarks_dict):
        """Set industry/market benchmarks"""
        self.market_data = benchmarks_dict
        return {'status': 'benchmarks_set', 'benchmark_count': len(benchmarks_dict)}
    
    def compare_metrics(self):
        """Compare company metrics against benchmarks"""
        try:
            comparison = {}
            
            for metric, company_value in self.company_data.items():
                if metric in self.market_data:
                    market_value = self.market_data[metric]
                    
                    # Calculate metrics
                    difference = company_value - market_value
                    pct_diff = (difference / market_value * 100) if market_value != 0 else 0
                    
                    # Determine status
                    if pct_diff > 10:
                        status = 'ABOVE_MARKET'
                    elif pct_diff < -10:
                        status = 'BELOW_MARKET'
                    else:
                        status = 'AT_MARKET'
                    
                    comparison[metric] = {
                        'company_value': round(company_value, 2),
                        'market_value': round(market_value, 2),
                        'difference': round(difference, 2),
                        'pct_difference': round(pct_diff, 2),
                        'status': status,
                        'percentile': 'top' if pct_diff > 0 else 'bottom'
                    }
            
            # Calculate overall score
            above_market = sum(1 for v in comparison.values() if v['status'] == 'ABOVE_MARKET')
            at_market = sum(1 for v in comparison.values() if v['status'] == 'AT_MARKET')
            below_market = sum(1 for v in comparison.values() if v['status'] == 'BELOW_MARKET')
            
            overall_health = (above_market * 3 + at_market * 2 + below_market * 1) / (len(comparison) * 3) * 100 if comparison else 0
            
            return {
                'comparison': comparison,
                'above_market': above_market,
                'at_market': at_market,
                'below_market': below_market,
                'overall_competitive_health': round(overall_health, 2),
                'recommendation': 'Strong' if overall_health > 70 else 'Good' if overall_health > 50 else 'Needs Improvement'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def market_positioning(self, company_metrics, market_segments):
        """Determine market positioning"""
        try:
            positioning = {}
            
            for segment, segment_data in market_segments.items():
                segment_pos = {}
                
                for metric, company_val in company_metrics.items():
                    if metric in segment_data:
                        segment_avg = segment_data[metric]['average']
                        segment_std = segment_data[metric]['std']
                        
                        # Z-score positioning
                        z_score = (company_val - segment_avg) / (segment_std + 1e-10)
                        
                        if z_score > 1.5:
                            position = 'PREMIUM'
                        elif z_score > 0.5:
                            position = 'ABOVE_AVERAGE'
                        elif z_score < -1.5:
                            position = 'BUDGET'
                        elif z_score < -0.5:
                            position = 'BELOW_AVERAGE'
                        else:
                            position = 'AVERAGE'
                        
                        segment_pos[metric] = {
                            'z_score': round(z_score, 2),
                            'position': position,
                            'vs_average': round((company_val - segment_avg) / segment_avg * 100, 2) if segment_avg != 0 else 0
                        }
                
                positioning[segment] = segment_pos
            
            return {
                'positioning': positioning,
                'market_analysis': 'positioning_complete'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def competitive_gap_analysis(self, company_data, top_competitors):
        """Identify gaps vs top competitors"""
        try:
            gaps = {}
            
            for competitor_name, competitor_metrics in top_competitors.items():
                competitor_gap = {}
                
                for metric, company_value in company_data.items():
                    if metric in competitor_metrics:
                        competitor_value = competitor_metrics[metric]
                        
                        gap = competitor_value - company_value
                        gap_pct = (gap / competitor_value * 100) if competitor_value != 0 else 0
                        
                        competitor_gap[metric] = {
                            'gap': round(gap, 2),
                            'gap_pct': round(gap_pct, 2),
                            'needs_improvement': gap > 0,
                            'improvement_potential': round(abs(gap), 2)
                        }
                
                gaps[competitor_name] = competitor_gap
            
            # Calculate average gap
            all_gaps = []
            for comp_gaps in gaps.values():
                for metric_gap in comp_gaps.values():
                    all_gaps.append(metric_gap['gap_pct'])
            
            avg_gap = np.mean(all_gaps) if all_gaps else 0
            
            return {
                'gaps_by_competitor': gaps,
                'average_gap_%': round(avg_gap, 2),
                'priority_improvements': 'high' if avg_gap > 10 else 'medium' if avg_gap > 5 else 'low'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def market_share_analysis(self, company_revenue, market_data):
        """Analyze market share and position"""
        try:
            total_market = sum(market_data.values())
            company_share = (company_revenue / total_market * 100) if total_market > 0 else 0
            
            # Ranking
            sorted_players = sorted(market_data.items(), key=lambda x: x[1], reverse=True)
            company_rank = len(sorted_players) + 1
            for rank, (player, revenue) in enumerate(sorted_players, 1):
                if revenue == company_revenue:
                    company_rank = rank
                    break
            
            # Market concentration
            top_3_share = sum([rev for _, rev in sorted_players[:3]]) / total_market * 100 if total_market > 0 else 0
            
            # Growth potential
            avg_player_share = 100 / len(market_data)
            share_vs_avg = company_share / avg_player_share
            
            return {
                'market_share_%': round(company_share, 2),
                'market_rank': company_rank,
                'total_market_size': total_market,
                'company_revenue': company_revenue,
                'top_3_market_share_%': round(top_3_share, 2),
                'share_vs_average': round(share_vs_avg, 2),
                'market_position': 'Leader' if company_share > 20 else 'Strong Contender' if company_share > 10 else 'Challenger' if company_share > 5 else 'Niche',
                'growth_opportunity': 'High' if share_vs_avg < 0.5 else 'Moderate' if share_vs_avg < 1 else 'Limited'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def performance_scorecard(self, metrics, weights=None):
        """Create weighted performance scorecard"""
        try:
            if weights is None:
                weights = {metric: 1/len(metrics) for metric in metrics}
            
            scorecard = {}
            total_score = 0
            
            for metric, value in metrics.items():
                if metric in weights:
                    weight = weights[metric]
                    score = min(100, max(0, value * 100 / 10))  # Normalize to 0-100
                    weighted_score = score * weight
                    
                    scorecard[metric] = {
                        'value': round(value, 2),
                        'score': round(score, 2),
                        'weight': weight,
                        'weighted_score': round(weighted_score, 2)
                    }
                    
                    total_score += weighted_score
            
            # Overall rating
            if total_score >= 80:
                rating = 'EXCELLENT'
            elif total_score >= 60:
                rating = 'GOOD'
            elif total_score >= 40:
                rating = 'FAIR'
            else:
                rating = 'NEEDS_IMPROVEMENT'
            
            return {
                'scorecard': scorecard,
                'overall_score': round(total_score, 2),
                'rating': rating
            }
        except Exception as e:
            return {'error': str(e)}


class MarketTrendAnalysis:
    """Analyze market trends and opportunities"""
    
    def __init__(self):
        self.market_data = []
    
    def trend_extraction(self, df, date_col, value_col):
        """Extract market trends over time"""
        try:
            df = df.sort_values(date_col)
            
            # Calculate trend using linear regression
            x = np.arange(len(df))
            y = df[value_col].values
            
            coeffs = np.polyfit(x, y, 2)
            trend = np.polyval(coeffs, x)
            
            # Calculate growth rate
            early_avg = np.mean(y[:len(y)//4])
            late_avg = np.mean(y[3*len(y)//4:])
            growth_rate = ((late_avg - early_avg) / early_avg * 100) if early_avg != 0 else 0
            
            # Volatility
            volatility = np.std(np.diff(y))
            
            return {
                'trend': trend.tolist(),
                'growth_rate_%': round(growth_rate, 2),
                'volatility': round(volatility, 2),
                'trend_direction': 'upward' if growth_rate > 5 else 'downward' if growth_rate < -5 else 'stable'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def market_opportunity_scoring(self, market_size, growth_rate, competition_level, entry_barriers):
        """Score market opportunities"""
        try:
            # Normalize inputs (0-10 scale)
            market_score = min(10, market_size / 100)
            growth_score = min(10, growth_rate)
            competition_score = (10 - competition_level)  # Lower competition is better
            entry_score = (10 - entry_barriers)  # Lower barriers are better
            
            # Calculate weighted opportunity score
            opportunity_score = (
                market_score * 0.3 +
                growth_score * 0.3 +
                competition_score * 0.2 +
                entry_score * 0.2
            )
            
            # Opportunity rating
            if opportunity_score >= 7:
                rating = 'EXCELLENT'
            elif opportunity_score >= 5:
                rating = 'GOOD'
            elif opportunity_score >= 3:
                rating = 'FAIR'
            else:
                rating = 'POOR'
            
            return {
                'opportunity_score': round(opportunity_score, 2),
                'rating': rating,
                'market_size_factor': round(market_score, 2),
                'growth_factor': round(growth_score, 2),
                'competition_factor': round(competition_score, 2),
                'entry_barrier_factor': round(entry_score, 2),
                'recommendation': 'High Priority' if opportunity_score >= 7 else 'Medium Priority' if opportunity_score >= 5 else 'Low Priority'
            }
        except Exception as e:
            return {'error': str(e)}
