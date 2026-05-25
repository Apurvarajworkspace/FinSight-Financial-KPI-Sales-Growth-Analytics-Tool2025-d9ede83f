"""
Market Basket Analysis Module - Association Rule Mining
Product/Service affinity analysis and cross-selling opportunities
"""

import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter


class MarketBasketAnalyzer:
    """Analyze product associations and cross-selling opportunities"""
    
    def __init__(self, min_support=0.01):
        self.min_support = min_support
        self.transactions = []
        self.itemsets = {}
        self.rules = []
    
    def prepare_transactions(self, df, transaction_col, product_col):
        """Prepare transaction data"""
        try:
            self.transactions = df.groupby(transaction_col)[product_col].apply(list).tolist()
            return {
                'transaction_count': len(self.transactions),
                'avg_items_per_transaction': np.mean([len(t) for t in self.transactions]),
                'unique_products': len(set([item for trans in self.transactions for item in trans])),
                'status': 'ready'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_support(self, itemset):
        """Calculate support for an itemset"""
        count = sum(1 for trans in self.transactions if set(itemset).issubset(set(trans)))
        return count / len(self.transactions) if self.transactions else 0
    
    def apriori_mining(self, max_itemset_size=3):
        """Mine frequent itemsets using Apriori algorithm"""
        try:
            all_items = set([item for trans in self.transactions for item in trans])
            itemsets = {}
            
            # 1-itemsets
            one_itemsets = {}
            for item in all_items:
                support = self.calculate_support([item])
                if support >= self.min_support:
                    one_itemsets[tuple([item])] = support
            
            itemsets[1] = one_itemsets
            previous_itemsets = one_itemsets
            
            # k-itemsets
            for k in range(2, max_itemset_size + 1):
                candidates = []
                items_list = list(previous_itemsets.keys())
                
                for i in range(len(items_list)):
                    for j in range(i + 1, len(items_list)):
                        union = tuple(sorted(set(items_list[i]) | set(items_list[j])))
                        if len(union) == k and union not in candidates:
                            candidates.append(union)
                
                k_itemsets = {}
                for candidate in candidates:
                    support = self.calculate_support(candidate)
                    if support >= self.min_support:
                        k_itemsets[candidate] = support
                
                if k_itemsets:
                    itemsets[k] = k_itemsets
                    previous_itemsets = k_itemsets
                else:
                    break
            
            self.itemsets = itemsets
            
            return {
                'frequent_itemsets': itemsets,
                'itemset_count': sum(len(v) for v in itemsets.values()),
                'largest_itemset_size': max(itemsets.keys()) if itemsets else 0,
                'status': 'mining_complete'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def generate_association_rules(self, min_confidence=0.5, min_lift=1.0):
        """Generate association rules from frequent itemsets"""
        try:
            rules = []
            
            for itemset_size, itemsets in self.itemsets.items():
                if itemset_size < 2:
                    continue
                
                for itemset, support in itemsets.items():
                    # Generate all possible rules
                    for i in range(1, len(itemset)):
                        for antecedent in combinations(itemset, i):
                            antecedent = tuple(sorted(antecedent))
                            consequent = tuple(sorted(set(itemset) - set(antecedent)))
                            
                            # Calculate metrics
                            antecedent_support = self.itemsets.get(len(antecedent), {}).get(antecedent, 0)
                            consequent_support = self.itemsets.get(len(consequent), {}).get(consequent, 0)
                            
                            if antecedent_support == 0 or consequent_support == 0:
                                continue
                            
                            confidence = support / antecedent_support
                            lift = support / (antecedent_support * consequent_support)
                            
                            if confidence >= min_confidence and lift >= min_lift:
                                rules.append({
                                    'antecedent': antecedent,
                                    'consequent': consequent,
                                    'support': round(support, 4),
                                    'confidence': round(confidence, 4),
                                    'lift': round(lift, 4),
                                    'leverage': round(support - (antecedent_support * consequent_support), 4)
                                })
            
            self.rules = sorted(rules, key=lambda x: x['lift'], reverse=True)
            
            return {
                'rules': self.rules,
                'rule_count': len(self.rules),
                'avg_confidence': np.mean([r['confidence'] for r in self.rules]) if self.rules else 0,
                'avg_lift': np.mean([r['lift'] for r in self.rules]) if self.rules else 0,
                'top_rules': self.rules[:10] if len(self.rules) >= 10 else self.rules
            }
        except Exception as e:
            return {'error': str(e)}
    
    def find_cross_sell_opportunities(self, bought_items, top_n=5):
        """Find cross-sell recommendations for given items"""
        try:
            recommendations = {}
            
            for rule in self.rules:
                if set(rule['antecedent']).issubset(set(bought_items)):
                    for item in rule['consequent']:
                        if item not in bought_items:
                            if item not in recommendations:
                                recommendations[item] = {
                                    'confidence': rule['confidence'],
                                    'lift': rule['lift'],
                                    'count': 1
                                }
                            else:
                                recommendations[item]['confidence'] += rule['confidence']
                                recommendations[item]['lift'] += rule['lift']
                                recommendations[item]['count'] += 1
            
            # Sort by combined score
            sorted_recs = sorted(
                recommendations.items(),
                key=lambda x: (x[1]['lift'] * x[1]['confidence']),
                reverse=True
            )[:top_n]
            
            return {
                'recommendations': [{'item': item, **metrics} for item, metrics in sorted_recs],
                'recommendation_count': len(sorted_recs),
                'avg_lift': np.mean([m['lift'] for _, m in sorted_recs]) if sorted_recs else 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def product_clustering(self, method='association'):
        """Cluster related products"""
        try:
            product_pairs = {}
            
            # Build product relationship graph
            for rule in self.rules:
                for ant in rule['antecedent']:
                    for cons in rule['consequent']:
                        pair = tuple(sorted([ant, cons]))
                        if pair not in product_pairs:
                            product_pairs[pair] = 0
                        product_pairs[pair] += rule['lift']
            
            # Group products by strong associations
            clusters = {}
            visited = set()
            
            for pair, strength in sorted(product_pairs.items(), key=lambda x: x[1], reverse=True):
                if pair[0] not in visited and pair[1] not in visited:
                    cluster_id = len(clusters)
                    clusters[cluster_id] = list(pair)
                    visited.add(pair[0])
                    visited.add(pair[1])
            
            return {
                'clusters': clusters,
                'cluster_count': len(clusters),
                'product_relationships': product_pairs,
                'top_associations': list(product_pairs.items())[:10]
            }
        except Exception as e:
            return {'error': str(e)}


class SequentialPatternMining:
    """Discover temporal patterns in customer behavior"""
    
    def __init__(self, min_support=0.1):
        self.min_support = min_support
        self.sequences = []
    
    def prepare_sequences(self, df, customer_col, item_col, date_col):
        """Prepare sequential data ordered by date"""
        try:
            df = df.sort_values(date_col)
            self.sequences = df.groupby(customer_col)[item_col].apply(list).tolist()
            return {
                'sequence_count': len(self.sequences),
                'avg_sequence_length': np.mean([len(s) for s in self.sequences]),
                'unique_items': len(set([item for seq in self.sequences for item in seq])),
                'status': 'ready'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def find_frequent_sequences(self, max_length=3):
        """Find frequent sequential patterns"""
        try:
            patterns = {}
            
            for length in range(1, max_length + 1):
                length_patterns = Counter()
                
                for sequence in self.sequences:
                    for i in range(len(sequence) - length + 1):
                        pattern = tuple(sequence[i:i+length])
                        length_patterns[pattern] += 1
                
                # Filter by support
                for pattern, count in length_patterns.items():
                    support = count / len(self.sequences)
                    if support >= self.min_support:
                        patterns[pattern] = {
                            'support': support,
                            'count': count
                        }
            
            sorted_patterns = sorted(patterns.items(), key=lambda x: x[1]['support'], reverse=True)
            
            return {
                'patterns': dict(sorted_patterns[:20]),
                'pattern_count': len(patterns),
                'top_patterns': sorted_patterns[:10]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def predict_next_purchase(self, customer_sequence, top_n=3):
        """Predict next purchase in sequence"""
        try:
            next_items = {}
            
            for sequence in self.sequences:
                for i in range(len(sequence) - 1):
                    if tuple(sequence[:i+1]) == tuple(customer_sequence):
                        next_item = sequence[i+1]
                        next_items[next_item] = next_items.get(next_item, 0) + 1
            
            if not next_items:
                return {
                    'predictions': [],
                    'confidence': 0,
                    'message': 'No matching sequences found'
                }
            
            total = sum(next_items.values())
            predictions = sorted(
                [(item, count/total) for item, count in next_items.items()],
                key=lambda x: x[1],
                reverse=True
            )[:top_n]
            
            return {
                'predictions': [{'item': item, 'probability': prob} for item, prob in predictions],
                'top_prediction': predictions[0][0] if predictions else None,
                'confidence': predictions[0][1] if predictions else 0
            }
        except Exception as e:
            return {'error': str(e)}
