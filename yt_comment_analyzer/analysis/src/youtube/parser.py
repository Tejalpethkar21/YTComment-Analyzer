import re
from urllib.parse import urlparse, parse_qs

class YouTubeURLParser:
    @staticmethod
    def extract_video_id(url):
       
        # Standard watch URL
        if 'youtube.com/watch' in url:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        
        # Short URL (youtu.be)
        if 'youtu.be' in url:
            path = urlparse(url).path
            return path[1:] if path else None
        
        # Embedded URL
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/live\/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None

    @staticmethod
    def is_valid_youtube_url(url):
        
        patterns = [
            r'^https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{11}',
            r'^https?://youtu\.be/[a-zA-Z0-9_-]{11}',
            r'^https?://(?:www\.)?youtube\.com/embed/[a-zA-Z0-9_-]{11}',
            r'^https?://(?:www\.)?youtube\.com/v/[a-zA-Z0-9_-]{11}',
            r'^https?://(?:www\.)?youtube\.com/shorts/[a-zA-Z0-9_-]{11}',
            r'^https?://(?:www\.)?youtube\.com/live/[a-zA-Z0-9_-]{11}'
        ]
        
        return any(re.match(pattern, url) for pattern in patterns)

    @staticmethod
    def normalize_url(url):

        video_id = YouTubeURLParser.extract_video_id(url)
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
        return None


def extract_video_id(url):
    """Standalone function for backward compatibility."""
    return YouTubeURLParser.extract_video_id(url)