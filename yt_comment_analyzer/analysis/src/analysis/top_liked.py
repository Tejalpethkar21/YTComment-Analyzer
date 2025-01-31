from youtube.api_client import YouTubeClient, CommentFetcher
from youtube.parser import YouTubeURLParser

class TopLikedComments:
    def __init__(self):
        self.client = YouTubeClient()
        self.fetcher = CommentFetcher(self.client)

    def get_top_liked_comments(self, video_id, top_n=10):
        results = self.fetcher.fetch_comments(video_id, limit=100)
        comments = self._extract_comments_with_likes(results)

        while len(comments) < top_n and "nextPageToken" in results:
            next_page_token = results["nextPageToken"]
            results = self.fetcher.fetch_comments(video_id, limit=100, page_token=next_page_token)
            comments.extend(self._extract_comments_with_likes(results))

        comments.sort(key=lambda x: x["like_count"], reverse=True)
        return comments[:top_n]

    def _extract_comments_with_likes(self, results):
        comments = []
        for item in results.get("items", []):
            comment = item["snippet"]["topLevelComment"]
            text = comment["snippet"]["textDisplay"]
            like_count = comment["snippet"].get("likeCount", 0)
            comments.append({
                "text": text,
                "like_count": like_count
            })
        return comments

