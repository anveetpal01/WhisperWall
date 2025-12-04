from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from schemas.post import PostCreate, PostResponse, PaginatedPostsResponse
from services.post_service import PostService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/posts", response_model=PostResponse, status_code=201)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db)
):
    """Create a new anonymous post"""
    try:
        service = PostService(db)
        new_post = service.create_post(post)
        logger.info(f"Post created: ID={new_post.id}")
        return new_post
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create post")


@router.get("/posts", response_model=PaginatedPostsResponse)
async def get_posts(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get all posts with pagination"""
    try:
        service = PostService(db)
        result = service.get_posts(page=page, limit=limit)
        return result
    except Exception as e:
        logger.error(f"Error fetching posts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch posts")


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific post by ID"""
    try:
        service = PostService(db)
        post = service.get_post_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching post {post_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch post")


@router.post("/posts/{post_id}/like", response_model=PostResponse)
async def like_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Like a post (increment like count)"""
    try:
        service = PostService(db)
        post = service.like_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        logger.info(f"Post {post_id} liked. Total likes: {post.likes}")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error liking post {post_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to like post")


@router.post("/posts/{post_id}/flag", response_model=PostResponse)
async def flag_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Flag a post for moderation"""
    try:
        service = PostService(db)
        post = service.flag_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        logger.warning(f"Post {post_id} flagged for moderation")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error flagging post {post_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to flag post")


@router.delete("/posts/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Delete a post"""
    try:
        service = PostService(db)
        success = service.delete_post(post_id)
        if not success:
            raise HTTPException(status_code=404, detail="Post not found")
        logger.info(f"Post {post_id} deleted")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting post {post_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete post")
