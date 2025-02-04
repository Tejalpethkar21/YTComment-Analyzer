import asyncio
import matplotlib.pyplot as plt
from youtube.api_client import YouTubeClient, CommentFetcher
from youtube.parser import YouTubeURLParser
from processing.cleaners import clean_text
from analysis.sentiment import SentimentAnalyzer
from analysis.emojis import EmojiAnalyzer
from analysis.translateAnalyzer import TranslateSentimentAnalyzer


class YouTubeCommentAnalyzer:
    def __init__(self):
        self.client = YouTubeClient()
        self.fetcher = CommentFetcher(self.client)
        self.sentiment = SentimentAnalyzer()  # English Sentiment Analyzer
        self.translated_sentiment = TranslateSentimentAnalyzer()  # Translated Sentiment Analyzer
        self.emoji = EmojiAnalyzer()

    async def analyze(self, video_url, comment_limit=100):
        video_id = YouTubeURLParser().extract_video_id(video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")

        # Fetch comments
        raw_comments = self.fetcher.fetch_comments(video_id, comment_limit)
        cleaned_comments = [clean_text(c) for c in raw_comments]

        # Perform sentiment analysis
        sentiment_vader = self.sentiment.analyze_vader(cleaned_comments)
        sentiment_textblob = self.sentiment.analyze_textblob(cleaned_comments)

        translated_vader = await self.translated_sentiment.analyze_vader(cleaned_comments)
        translated_textblob = await self.translated_sentiment.analyze_textblob(cleaned_comments)

        return {
            'sentiment': {
                'vader': sentiment_vader,
                'textblob': sentiment_textblob
            },
            'translated_sentiment': {
                'vader': translated_vader,
                'textblob': translated_textblob
            },
            'emojis': self.emoji.top_emojis(raw_comments),
            'total_comments': len(cleaned_comments)
        }


def display_sentiment(sentiment, translated_sentiment):
    print("\nSentiment Analysis (Original Text):")
    for engine, data in sentiment.items():
        print(f"\n{engine.title()} Results:")
        print(f"Overall Score: {data['overall']:.2f}")
        for category, percentage in data['breakdown'].items():
            print(f"{category.title()}: {percentage}%")

    print("\nSentiment Analysis (Translated Text):")
    for engine, data in translated_sentiment.items():
        print(f"\n{engine.title()} Results:")
        print(f"Overall Score: {data['overall']:.2f}")
        for category, percentage in data['breakdown'].items():
            print(f"{category.title()}: {percentage}%")


def display_emojis(emojis):
    print("\nTop Emojis:")
    for emoji, count in emojis:
        print(f"{emoji}: {count} times")


def show_visualizations(results):
    labels = list(results['sentiment']['vader']['breakdown'].keys())
    sizes = list(results['sentiment']['vader']['breakdown'].values())

    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Sentiment Distribution (VADER)")
    plt.show()


async def main():
    analyzer = YouTubeCommentAnalyzer()

    video_url = input("Enter YouTube video URL: ")
    comment_limit = int(input("Number of comments to analyze (max 5000): "))

    results = await analyzer.analyze(video_url, comment_limit)

    display_sentiment(results['sentiment'], results['translated_sentiment'])
    display_emojis(results['emojis'])
    show_visualizations(results)


if __name__ == "__main__":
    asyncio.run(main())  # Run async function properly
