from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import statistics

class SentimentAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()
        self.categories = [
            'positive', 'wpositive', 'spositive',
            'neutral',
            'negative', 'wnegative', 'snegative'
        ]
    
    def analyze_vader(self, comments):
        return self._analyze(comments, 'vader')
    
    def analyze_textblob(self, comments):
        return self._analyze(comments, 'textblob')
    
    def _analyze(self, comments, engine):
        results = {category: 0 for category in self.categories}
        scores = []
        
        for comment in comments:
            if engine == 'vader':
                score = self.sid.polarity_scores(comment)['compound']
            else:
                score = TextBlob(comment).sentiment.polarity
            
            scores.append(score)
            self._categorize(results, score)
        
        return self._format_results(results, scores, len(comments))
    
    def _categorize(self, results, score):
        if score == 0:
            results['neutral'] += 1
        elif 0 < score <= 0.3:
            results['wpositive'] += 1
        elif 0.3 < score <= 0.6:
            results['positive'] += 1
        elif 0.6 < score <= 1:
            results['spositive'] += 1
        elif -0.3 < score <= 0:
            results['wnegative'] += 1
        elif -0.6 < score <= -0.3:
            results['negative'] += 1
        elif -1 <= score <= -0.6:
            results['snegative'] += 1
    
    def _format_results(self, results, scores, total):
        return {
            'overall': statistics.mean(scores),
            'breakdown': {
                category: round((count / total) * 100, 2)
                for category, count in results.items()
            },
            'samples': len(scores)
        }