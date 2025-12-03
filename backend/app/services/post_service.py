from sqlalchemy.orm import Session
from sqlalchemy import desc
import math

from app.models.post import Post
from app.schemas.post import PostCreate, PaginatedPostsResponse
from app.config import settings


class PostService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_post(self, post_data: PostCreate) -> Post:
        """Create a new post"""
        if len(post_data.content) > settings.MAX_POST_LENGTH:
            raise ValueError(f"Post exceeds maximum length of {settings.MAX_POST_LENGTH} characters")
        
        db_post = Post(
            content=post_data.content,
            author_alias=post_data.author_alias or "Anonymous"
        )
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post
    
    def get_posts(self, page: int = 1, limit: int = 20) -> PaginatedPostsResponse:
        """Get all posts with pagination"""
        # Get total count
        total = self.db.query(Post).count()
        
        # Calculate pagination
        total_pages = math.ceil(total / limit)
        offset = (page - 1) * limit
        
        # Fetch posts
        posts = (
            self.db.query(Post)
            .order_by(desc(Post.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        return PaginatedPostsResponse(
            posts=posts,
            total=total,
            page=page,
            pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )
    
    def get_post_by_id(self, post_id: int) -> Post:
        """Get a single post by ID"""
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    def like_post(self, post_id: int) -> Post:
        """Increment like count for a post"""
        post = self.get_post_by_id(post_id)
        if post:
            post.likes += 1
            self.db.commit()
            self.db.refresh(post)
        return post
    
    def flag_post(self, post_id: int) -> Post:
        """Flag a post for moderation"""
        post = self.get_post_by_id(post_id)
        if post:
            post.is_flagged = True
            self.db.commit()
            self.db.refresh(post)
        return post
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        post = self.get_post_by_id(post_id)
        if post:
            self.db.delete(post)
            self.db.commit()
            return True
        return False