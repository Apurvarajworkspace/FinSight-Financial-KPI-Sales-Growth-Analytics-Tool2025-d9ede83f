"""
Customer Segmentation & RFM Analysis Module
Advanced customer analytics: RFM analysis, K-means clustering, customer value scoring
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from datetime import datetime, timedelta


class RFMAnalyzer:
    """RFM (Recency, Frequency, Monetary) Analysis for customer segmentation"""
    
    def __init__(self):
        self.rfm_data = None
        self.segments = {}
    
    def calculate_rfm(self, df, customer_col='customer_id', date_col='date', amount_col='amount'):
        """
        Calculate RFM metrics for each customer
        
        Args:
            df: Transaction dataframe
            customer_col: Customer ID column
            date_col: Date column
            amount_col: Transaction amount column
        
        Returns:
            RFM dataframe
        """
        # Reference date (max date in data)
        max_date = pd.to_datetime(df[date_col]).max()
        
        # Calculate RFM
        rfm = df.groupby(customer_col).agg({
            date_col: lambda x: (max_date - pd.to_datetime(x).max()).days,  # Recency
            customer_col: 'count',  # Frequency
            amount_col: 'sum'  # Monetary
        })
        
        rfm.columns = ['Recency', 'Frequency', 'Monetary']
        
        # Calculate quartiles for scoring
        rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1], duplicates='drop')
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4], duplicates='drop')
        rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), q=4, labels=[1, 2, 3, 4], duplicates='drop')
        
        # Overall RFM score
        rfm['RFM_Score'] = rfm['R_Score'].astype(int).astype(str) + \
                          rfm['F_Score'].astype(int).astype(str) + \
                          rfm['M_Score'].astype(int).astype(str)
        
        # Customer value rating
        rfm['Combined_Score'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)
        
        self.rfm_data = rfm.sort_values('Combined_Score', ascending=False)
        return self.rfm_data
    
    def segment_customers(self, rfm_data=None):
        """
        Segment customers based on RFM scores
        
        Args:
            rfm_data: RFM dataframe
        
        Returns:
            Segmentation with labels
        """
        if rfm_data is not None:
            self.rfm_data = rfm_data
        
        if self.rfm_data is None:
            raise ValueError("No RFM data available")
        
        rfm = self.rfm_data.copy()
        
        # Segmentation logic
        def assign_segment(row):
            r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
            combined = row['Combined_Score']
            
            if combined >= 10:
                return 'Champions'
            elif combined >= 8 and r >= 3:
                return 'Loyal Customers'
            elif combined >= 8 and f >= 3:
                return 'Frequent Buyers'
            elif m >= 3 and f < 2:
                return 'Big Spenders'
            elif combined >= 6 and r >= 3:
                return 'Potential Loyalists'
            elif combined >= 6:
                return 'At Risk'
            elif r <= 2 and f <= 2:
                return 'Lost'
            else:
                return 'New Customers'
        
        rfm['Segment'] = rfm.apply(assign_segment, axis=1)
        
        # Store segments
        self.segments = rfm.groupby('Segment').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': ['mean', 'sum', 'count']
        }).round(2)
        
        return rfm
    
    def get_segment_recommendations(self):
        """Get actionable recommendations for each segment"""
        
        recommendations = {
            'Champions': {
                'description': 'Best customers - loyal and high-value',
                'actions': [
                    'Reward loyalty with exclusive offers',
                    'Engage in VIP programs',
                    'Request reviews and referrals',
                    'Involve in product development'
                ],
                'priority': 'CRITICAL'
            },
            'Loyal Customers': {
                'description': 'High frequency and consistent buyers',
                'actions': [
                    'Maintain relationship with regular communication',
                    'Upsell complementary products',
                    'Create loyalty program tiers',
                    'Gather feedback'
                ],
                'priority': 'HIGH'
            },
            'Frequent Buyers': {
                'description': 'Purchase often but may not be high-value',
                'actions': [
                    'Increase transaction value through cross-selling',
                    'Bundle products for higher AOV',
                    'Create tiered pricing',
                    'Personalized recommendations'
                ],
                'priority': 'HIGH'
            },
            'Big Spenders': {
                'description': 'High value but low frequency',
                'actions': [
                    'Personal account management',
                    'Premium customer service',
                    'Exclusive products/services',
                    'Special event invitations'
                ],
                'priority': 'HIGH'
            },
            'Potential Loyalists': {
                'description': 'Recently active with moderate value',
                'actions': [
                    'Nurture relationship with targeted offers',
                    'Create entry-level loyalty programs',
                    'Personalized communication',
                    'Early access to new products'
                ],
                'priority': 'MEDIUM'
            },
            'At Risk': {
                'description': 'Decline in activity or value',
                'actions': [
                    'Send win-back campaigns',
                    'Offer special discounts',
                    'Request feedback on satisfaction',
                    'Re-engagement campaigns'
                ],
                'priority': 'MEDIUM'
            },
            'Lost': {
                'description': 'No recent activity, low engagement',
                'actions': [
                    'Powerful re-engagement campaigns',
                    'Significant offers/discounts',
                    'Apologize for service gaps',
                    'Survey for improvement areas'
                ],
                'priority': 'LOW'
            },
            'New Customers': {
                'description': 'Recent but limited purchase history',
                'actions': [
                    'Welcome series campaigns',
                    'Educate on product features',
                    'First-purchase incentives',
                    'Build initial loyalty'
                ],
                'priority': 'MEDIUM'
            }
        }
        
        return recommendations


class CustomerClusterer:
    """Advanced customer clustering using K-means"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.clusters = None
    
    def prepare_features(self, df):
        """Prepare customer features for clustering"""
        
        features = []
        customer_ids = []
        
        for customer in df['customer_id'].unique():
            customer_data = df[df['customer_id'] == customer]
            
            customer_ids.append(customer)
            features.append({
                'total_spent': customer_data['amount'].sum(),
                'transaction_count': len(customer_data),
                'avg_transaction': customer_data['amount'].mean(),
                'std_transaction': customer_data['amount'].std() or 0,
                'min_transaction': customer_data['amount'].min(),
                'max_transaction': customer_data['amount'].max(),
                'days_active': (pd.to_datetime(customer_data['date']).max() - 
                              pd.to_datetime(customer_data['date']).min()).days + 1,
            })
        
        feature_df = pd.DataFrame(features, index=customer_ids)
        feature_df = feature_df.fillna(0)
        
        return feature_df
    
    def cluster_customers(self, df, n_clusters=4, features=None):
        """
        Perform K-means clustering on customers
        
        Args:
            df: Transaction dataframe
            n_clusters: Number of clusters
            features: Feature dataframe or None to auto-generate
        
        Returns:
            Clustered dataframe
        """
        if features is None:
            features = self.prepare_features(df)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(features)
        
        # Fit K-means
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = self.model.fit_predict(X_scaled)
        
        # Assign clusters
        features['Cluster'] = clusters
        features['Cluster_Label'] = ['Cluster_' + str(c) for c in clusters]
        
        self.clusters = features
        return features
    
    def get_cluster_profiles(self):
        """Get profile of each cluster"""
        
        if self.clusters is None:
            raise ValueError("No clusters available")
        
        profiles = self.clusters.groupby('Cluster').agg({
            'total_spent': ['mean', 'sum', 'count'],
            'transaction_count': 'mean',
            'avg_transaction': 'mean',
            'days_active': 'mean'
        }).round(2)
        
        return profiles
    
    def calculate_cluster_metrics(self):
        """Calculate clustering quality metrics"""
        
        if self.model is None or self.clusters is None:
            raise ValueError("No clustering model available")
        
        # Silhouette score would require another import, but we can use inertia
        inertia = self.model.inertia_
        
        n_clusters = len(self.clusters['Cluster'].unique())
        n_samples = len(self.clusters)
        
        return {
            'n_clusters': n_clusters,
            'n_samples': n_samples,
            'inertia': inertia,
            'avg_samples_per_cluster': n_samples / n_clusters,
            'silhouette_score': 'Calculate using silhouette_score if needed'
        }


class CustomerValueScorer:
    """Score and rank customers by value"""
    
    @staticmethod
    def calculate_clv_based_score(df, customer_col='customer_id', amount_col='amount', 
                                   date_col='date', lookback_months=12):
        """
        Calculate Customer Lifetime Value-based score
        
        Args:
            df: Transaction dataframe
            customer_col: Customer ID column
            amount_col: Amount column
            date_col: Date column
            lookback_months: Period to analyze
        
        Returns:
            Scored dataframe
        """
        # Filter recent data
        cutoff_date = pd.to_datetime(df[date_col]).max() - timedelta(days=lookback_months*30)
        recent_df = df[pd.to_datetime(df[date_col]) >= cutoff_date]
        
        # Calculate metrics
        metrics = recent_df.groupby(customer_col).agg({
            amount_col: ['sum', 'mean', 'count'],
            date_col: [lambda x: (pd.to_datetime(x).max() - pd.to_datetime(x).min()).days + 1, 'count']
        })
        
        metrics.columns = ['total_revenue', 'avg_transaction_value', 'transaction_count', 
                          'customer_lifetime', 'purchase_frequency']
        
        # Calculate scores (0-100)
        total_revenue_max = metrics['total_revenue'].max()
        avg_value_max = metrics['avg_transaction_value'].max()
        frequency_max = metrics['purchase_frequency'].max()
        
        metrics['revenue_score'] = (metrics['total_revenue'] / total_revenue_max * 100).fillna(0)
        metrics['value_score'] = (metrics['avg_transaction_value'] / avg_value_max * 100).fillna(0)
        metrics['frequency_score'] = (metrics['purchase_frequency'] / frequency_max * 100).fillna(0)
        
        # Weighted composite score
        metrics['customer_value_score'] = (
            metrics['revenue_score'] * 0.5 +
            metrics['value_score'] * 0.3 +
            metrics['frequency_score'] * 0.2
        ).round(2)
        
        return metrics.sort_values('customer_value_score', ascending=False)
    
    @staticmethod
    def predict_churn_risk(df, customer_col='customer_id', date_col='date', 
                           amount_col='amount', recent_days=30):
        """
        Predict churn risk based on recent activity
        
        Args:
            df: Transaction dataframe
            recent_days: Days to consider for recency
        
        Returns:
            Churn risk scores
        """
        max_date = pd.to_datetime(df[date_col]).max()
        cutoff = max_date - timedelta(days=recent_days)
        
        churn_risk = []
        
        for customer in df[customer_col].unique():
            customer_data = df[df[customer_col] == customer]
            last_purchase = pd.to_datetime(customer_data[date_col]).max()
            
            # Days since last purchase
            days_inactive = (max_date - last_purchase).days
            
            # Historical activity
            avg_frequency = len(customer_data) / ((pd.to_datetime(customer_data[date_col]).max() - 
                                                   pd.to_datetime(customer_data[date_col]).min()).days + 1)
            
            # Trend (recent vs historical)
            recent_purchases = len(customer_data[pd.to_datetime(customer_data[date_col]) >= cutoff])
            historical_avg = len(customer_data) / ((pd.to_datetime(customer_data[date_col]).max() - 
                                                    pd.to_datetime(customer_data[date_col]).min()).days + 1) * recent_days
            
            trend_decline = max(0, (historical_avg - recent_purchases) / (historical_avg + 1e-8))
            
            # Calculate churn risk (0-100)
            recency_risk = min(100, (days_inactive / (recent_days * 2)) * 100)
            trend_risk = trend_decline * 100
            
            churn_risk_score = (recency_risk * 0.6 + trend_risk * 0.4)
            
            churn_risk.append({
                'customer_id': customer,
                'days_inactive': days_inactive,
                'recent_purchases': recent_purchases,
                'churn_risk_score': round(churn_risk_score, 2),
                'risk_level': 'HIGH' if churn_risk_score >= 70 else ('MEDIUM' if churn_risk_score >= 40 else 'LOW')
            })
        
        return pd.DataFrame(churn_risk).sort_values('churn_risk_score', ascending=False)
