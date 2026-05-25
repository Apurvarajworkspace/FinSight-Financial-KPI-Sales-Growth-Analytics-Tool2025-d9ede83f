"""
Advanced NLP & Sentiment Analysis Module
Analyze customer feedback, reviews, and text data for insights
"""

import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter
import re


class TextPreprocessor:
    """Text preprocessing utilities"""
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Convert to lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.strip()
    
    @staticmethod
    def extract_keywords(text, top_n=10):
        """Extract top keywords from text"""
        words = text.split()
        # Simple keyword frequency
        word_freq = Counter(words)
        return word_freq.most_common(top_n)
    
    @staticmethod
    def tokenize(text):
        """Tokenize text into words"""
        return text.split()


class SentimentAnalyzer:
    """Sentiment analysis for customer feedback"""
    
    def __init__(self):
        # Simple lexicon-based sentiment
        self.positive_words = {'good', 'great', 'excellent', 'amazing', 'love', 'perfect', 
                              'wonderful', 'fantastic', 'best', 'satisfied', 'happy'}
        self.negative_words = {'bad', 'terrible', 'awful', 'hate', 'poor', 'worst', 
                              'horrible', 'disappointing', 'angry', 'frustrated'}
        self.analysis_history = []
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text (positive, negative, neutral)"""
        clean_text = TextPreprocessor.clean_text(text)
        words = set(TextPreprocessor.tokenize(clean_text))
        
        positive_count = len(words & self.positive_words)
        negative_count = len(words & self.negative_words)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            score = min(positive_count / len(words), 1.0) if words else 0
        elif negative_count > positive_count:
            sentiment = 'negative'
            score = min(negative_count / len(words), 1.0) if words else 0
        else:
            sentiment = 'neutral'
            score = 0.5
        
        result = {
            'text': text[:100],
            'sentiment': sentiment,
            'score': score,
            'positive_words': positive_count,
            'negative_words': negative_count,
            'timestamp': datetime.now().isoformat()
        }
        self.analysis_history.append(result)
        return result
    
    def get_sentiment_distribution(self):
        """Get distribution of sentiments"""
        if not self.analysis_history:
            return {}
        
        sentiments = [r['sentiment'] for r in self.analysis_history]
        distribution = Counter(sentiments)
        return {
            'positive': distribution.get('positive', 0),
            'negative': distribution.get('negative', 0),
            'neutral': distribution.get('neutral', 0),
            'total': len(sentiments)
        }
    
    def get_sentiment_trends(self):
        """Get sentiment trends over time"""
        if not self.analysis_history:
            return []
        
        grouped = {}
        for entry in self.analysis_history:
            date = entry['timestamp'][:10]
            if date not in grouped:
                grouped[date] = []
            grouped[date].append(entry['sentiment'])
        
        trends = []
        for date, sentiments in sorted(grouped.items()):
            distribution = Counter(sentiments)
            trends.append({
                'date': date,
                'positive_pct': (distribution['positive'] / len(sentiments) * 100) if sentiments else 0,
                'negative_pct': (distribution['negative'] / len(sentiments) * 100) if sentiments else 0,
                'neutral_pct': (distribution['neutral'] / len(sentiments) * 100) if sentiments else 0
            })
        return trends


class EntityExtractor:
    """Extract entities from text (customers, products, locations)"""
    
    def __init__(self):
        self.entities = {}
        self.entity_frequency = Counter()
    
    def extract_entities(self, text, entity_type='product'):
        """Extract entities of specific type"""
        # Simple entity extraction (can be enhanced with NER models)
        clean_text = TextPreprocessor.clean_text(text)
        words = TextPreprocessor.tokenize(clean_text)
        
        # For demo: consider capitalized words or specific patterns
        entities = [w for w in words if len(w) > 3]  # Simple heuristic
        
        return {
            'text': text[:100],
            'entity_type': entity_type,
            'entities': entities,
            'count': len(entities),
            'timestamp': datetime.now().isoformat()
        }
    
    def track_entity(self, entity, entity_type):
        """Track entity mentions"""
        key = f"{entity_type}:{entity}"
        self.entity_frequency[key] += 1
        return {'entity': entity, 'type': entity_type, 'frequency': self.entity_frequency[key]}
    
    def get_entity_statistics(self):
        """Get entity statistics"""
        entities_by_type = {}
        for key, count in self.entity_frequency.items():
            entity_type, entity = key.split(':', 1)
            if entity_type not in entities_by_type:
                entities_by_type[entity_type] = []
            entities_by_type[entity_type].append({'entity': entity, 'mentions': count})
        
        return entities_by_type


class FeedbackAnalyzer:
    """Analyze customer feedback and reviews"""
    
    def __init__(self, sentiment_analyzer, entity_extractor):
        self.sentiment = sentiment_analyzer
        self.entity = entity_extractor
        self.feedback_collection = []
        self.issue_tracker = {}
    
    def analyze_feedback(self, feedback_id, text, source='review'):
        """Analyze customer feedback"""
        sentiment_result = self.sentiment.analyze_sentiment(text)
        entities = self.entity.extract_entities(text)
        
        feedback = {
            'feedback_id': feedback_id,
            'source': source,  # review, survey, support_ticket, social_media
            'text': text,
            'sentiment': sentiment_result['sentiment'],
            'sentiment_score': sentiment_result['score'],
            'entities': entities['entities'],
            'analyzed_at': datetime.now().isoformat()
        }
        self.feedback_collection.append(feedback)
        return feedback
    
    def identify_issues(self):
        """Identify and categorize issues from feedback"""
        issues = {}
        for feedback in self.feedback_collection:
            if feedback['sentiment'] == 'negative':
                key = 'issue'
                if key not in issues:
                    issues[key] = []
                issues[key].append(feedback)
        
        return {
            'total_negative_feedback': len(issues.get('issue', [])),
            'unique_issues': len(set(str(f['entities']) for f in issues.get('issue', [])))
        }
    
    def get_feedback_summary(self):
        """Get comprehensive feedback summary"""
        total = len(self.feedback_collection)
        if total == 0:
            return {}
        
        sentiment_dist = self.sentiment.get_sentiment_distribution()
        issues = self.identify_issues()
        
        return {
            'total_feedback': total,
            'sentiment_distribution': sentiment_dist,
            'satisfaction_rate': ((sentiment_dist.get('positive', 0) / total) * 100) if total else 0,
            'issues_identified': issues['total_negative_feedback'],
            'average_sentiment_score': np.mean([f['sentiment_score'] for f in self.feedback_collection])
        }


def run_nlp_sentiment_demo():
    """Demo function for NLP and sentiment analysis"""
    print("\n" + "="*70)
    print("NLP & SENTIMENT ANALYSIS DEMO")
    print("="*70)
    
    # Initialize NLP components
    sentiment = SentimentAnalyzer()
    entity = EntityExtractor()
    feedback_analyzer = FeedbackAnalyzer(sentiment, entity)
    
    # 1. Sentiment analysis
    print("\n[1] Sentiment Analysis...")
    print("-" * 70)
    reviews = [
        "This product is absolutely amazing! I love it!",
        "Terrible quality and poor customer service. Very disappointed.",
        "It's okay, nothing special but does the job.",
        "Excellent product, highly recommended!",
        "Worst purchase ever. Total waste of money."
    ]
    
    for review in reviews:
        feedback_analyzer.analyze_feedback(f'FB-{len(feedback_analyzer.feedback_collection)}', review)
    
    print(f"[DONE] Analyzed {len(feedback_analyzer.feedback_collection)} reviews")
    dist = sentiment.get_sentiment_distribution()
    print(f"[DONE] Sentiment Distribution: Positive: {dist['positive']}, Negative: {dist['negative']}, Neutral: {dist['neutral']}")
    
    # 2. Entity extraction
    print("\n[2] Entity Extraction...")
    print("-" * 70)
    for review in reviews[:3]:
        entity.extract_entities(review, 'product')
        entity.track_entity('product_name', 'product')
    entity_stats = entity.get_entity_statistics()
    print(f"[DONE] Entity Types Extracted: {len(entity_stats)}")
    
    # 3. Issue identification
    print("\n[3] Issue Identification...")
    print("-" * 70)
    issues = feedback_analyzer.identify_issues()
    print(f"[DONE] Negative Feedback Found: {issues['total_negative_feedback']}")
    print(f"[DONE] Unique Issues: {issues['unique_issues']}")
    
    # 4. Feedback summary
    print("\n[4] Feedback Summary Report...")
    print("-" * 70)
    summary = feedback_analyzer.get_feedback_summary()
    print(f"[DONE] Total Feedback: {summary['total_feedback']}")
    print(f"[DONE] Satisfaction Rate: {summary['satisfaction_rate']:.1f}%")
    print(f"[DONE] Average Sentiment Score: {summary['average_sentiment_score']:.3f}")
    print(f"[DONE] Issues to Address: {summary['issues_identified']}")
    
    # 5. Sentiment trends
    print("\n[5] Sentiment Trends...")
    print("-" * 70)
    trends = sentiment.get_sentiment_trends()
    print(f"[DONE] Trend Data Points: {len(trends)}")
    if trends:
        latest = trends[-1]
        print(f"[DONE] Latest Trend - Positive: {latest['positive_pct']:.1f}%, Negative: {latest['negative_pct']:.1f}%")
    
    print("\n" + "="*70)
    print("[DONE] NLP & SENTIMENT ANALYSIS DEMO COMPLETED")
    print("="*70)
