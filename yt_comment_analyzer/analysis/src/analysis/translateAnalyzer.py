from aiogoogletrans import Translator
import asyncio
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import statistics
from langdetect import detect

class TranslateSentimentAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()
        self.translator = Translator()  # Asynchronous Translator
        self.categories = [
            'positive', 'wpositive', 'spositive',
            'neutral',
            'negative', 'wnegative', 'snegative'
        ]
    
    async def analyze_vader(self, comments):
        return await self._analyze(comments, 'vader')
    
    async def analyze_textblob(self, comments):
        return await self._analyze(comments, 'textblob')
    
    async def _analyze(self, comments, engine):
        results = {category: 0 for category in self.categories}
        scores = []
        
        # Translate all comments asynchronously
        translated_comments = await asyncio.gather(*[self._translate_to_english(c) for c in comments])

        for translated_comment in translated_comments:
            if engine == 'vader':
                score = self.sid.polarity_scores(translated_comment)['compound']
            else:
                score = TextBlob(translated_comment).sentiment.polarity
            
            scores.append(score)
            self._categorize(results, score)
        
        return self._format_results(results, scores, len(comments))
    
    async def _translate_to_english(self, text):
        """Asynchronously translates text to English."""
        try:
            detected_lang = detect(text)
            if detected_lang != 'en':
                translated_text = await self.translator.translate(text, dest='en')
                return translated_text.text if translated_text else text  # Await ensures async handling
            return text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
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
            'overall': statistics.mean(scores) if scores else 0,
            'breakdown': {
                category: round((count / total) * 100, 2) if total > 0 else 0
                for category, count in results.items()
            },
            'samples': len(scores)
        }
