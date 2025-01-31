import emoji
from collections import Counter

class EmojiAnalyzer:

    @staticmethod
    def extract_emojis(text):
       
        return [char for char in text if char in emoji.EMOJI_DATA]

    @staticmethod
    def count_emojis(texts):
        
        emoji_counter = Counter()
        for text in texts:
            emojis = EmojiAnalyzer.extract_emojis(text)
            emoji_counter.update(emojis)
        return emoji_counter

    @staticmethod
    def top_emojis(texts, top_n=5):
       
        emoji_counter = EmojiAnalyzer.count_emojis(texts)
        return emoji_counter.most_common(top_n)

    @staticmethod
    def emoji_sentiment_analysis(texts):
        
        emoji_sentiment = {}
        for text in texts:
            emojis = EmojiAnalyzer.extract_emojis(text)
            for emoji_char in emojis:
                # Use emoji's built-in sentiment data (if available)
                sentiment = emoji.EMOJI_DATA.get(emoji_char, {}).get('sentiment', 0)
                emoji_sentiment[emoji_char] = emoji_sentiment.get(emoji_char, 0) + sentiment
        return emoji_sentiment

    @staticmethod
    def replace_emojis(text, replacement=""):

        return emoji.replace_emoji(text, replacement=replacement)
