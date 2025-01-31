from youtube.api_client import YouTubeClient, CommentFetcher
from youtube.parser import YouTubeURLParser
from processing.cleaners import clean_text
from analysis.sentiment import SentimentAnalyzer
from analysis.emojis import EmojiAnalyzer
import matplotlib.pyplot as plt

class YouTubeCommentAnalyzer:
    def __init__(self):
        self.client = YouTubeClient()
        self.fetcher = CommentFetcher(self.client)
        self.sentiment = SentimentAnalyzer()
        self.emoji = EmojiAnalyzer()
    
    def analyze(self, video_url, comment_limit=100):
        video_id = YouTubeURLParser().extract_video_id(video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
        
        raw_comments = self.fetcher.fetch_comments(video_id, comment_limit)
        cleaned_comments = [clean_text(c) for c in raw_comments]
        
        return {
            'sentiment': {
                'vader': self.sentiment.analyze_vader(cleaned_comments),
                'textblob': self.sentiment.analyze_textblob(cleaned_comments)
            },
            'emojis': self.emoji.top_emojis(raw_comments),
            'total_comments': len(cleaned_comments)
        }

def _display_sentiment(sentiment):
    print("\nSentiment Analysis:")
    for engine, data in sentiment.items():
        print(f"\n{engine.title()} Results:")
        print(f"Overall Score: {data['overall']:.2f}")
        for category, percentage in data['breakdown'].items():
            print(f"{category.title()}: {percentage}%")

def _display_emojis(emojis):
    print("\nTop Emojis:")
    for emoji, count in emojis:
        print(f"{emoji}: {count} times")

def _show_visualizations(results):
    # Pie chart example
    labels = list(results['sentiment']['vader']['breakdown'].keys())
    sizes = list(results['sentiment']['vader']['breakdown'].values())
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Sentiment Distribution (VADER)")
    plt.show()

def main():
    analyzer = YouTubeCommentAnalyzer()
    video_url = input("Enter YouTube video URL: ")
    comment_limit = int(input("Number of comments to analyze (max 5000): "))
    
    results = analyzer.analyze(video_url, comment_limit)
    
    # Display results
    print(f"\nAnalyzed {results['total_comments']} comments")
    _display_sentiment(results['sentiment'])
    _display_emojis(results['emojis'])
    _show_visualizations(results)

if __name__ == "__main__":
    main()