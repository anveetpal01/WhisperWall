import requests
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def create_post(self, content: str, author_alias: str = "Anonymous") -> Dict:
        """Create a new post"""
        try:
            response = self.session.post(
                f"{self.base_url}/posts",
                json={"content": content, "author_alias": author_alias},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating post: {e}")
            raise Exception(f"Failed to create post: {str(e)}")
    
    def get_posts(self, page: int = 1, limit: int = 20) -> Dict:
        """Get paginated posts"""
        try:
            response = self.session.get(
                f"{self.base_url}/posts",
                params={"page": page, "limit": limit},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching posts: {e}")
            raise Exception(f"Failed to fetch posts: {str(e)}")
    
    def like_post(self, post_id: int) -> Dict:
        """Like a post"""
        try:
            response = self.session.post(
                f"{self.base_url}/posts/{post_id}/like",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error liking post: {e}")
            raise Exception(f"Failed to like post: {str(e)}")
    
    def flag_post(self, post_id: int) -> Dict:
        """Flag a post"""
        try:
            response = self.session.post(
                f"{self.base_url}/posts/{post_id}/flag",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error flagging post: {e}")
            raise Exception(f"Failed to flag post: {str(e)}")