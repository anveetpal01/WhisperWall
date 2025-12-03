from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    author_alias: Optional[str] = Field(default="Anonymous", max_length=50)
    
    @validator('content')
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Content cannot be empty or only whitespace')
        return v.strip()


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=5000)
    author_alias: Optional[str] = Field(None, max_length=50)


class PostResponse(PostBase):
    id: int
    likes: int
    is_flagged: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PostLike(BaseModel):
    post_id: int


class PaginatedPostsResponse(BaseModel):
    posts: list[PostResponse]
    total: int
    page: int
    pages: int
    has_next: bool
    has_prev: bool