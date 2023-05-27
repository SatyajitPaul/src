from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from slugify import slugify
from .util import PrivacyType


from database import Base
#Post Table
class Post(Base):
    __tablename__ = 'posts'
    id = mapped_column(Integer, primary_key=True)
    content = mapped_column(String(1024))
    like_count = mapped_column(Integer, default=0)
    dislike_count = mapped_column(Integer, default=0)
    comment_count = mapped_column(Integer, default=0)
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    modified_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_anonymous = mapped_column(Boolean, default=False)
    privacy_type = mapped_column(Enum(PrivacyType), default=PrivacyType.PUBLIC)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")
    
    images = relationship("PostImage", back_populates="post")

    #SEO Fields for posts
    meta_title = mapped_column(String)
    meta_description = mapped_column(String)
    slug = mapped_column(String)

    @validates('content')
    def validate_content(self, key, content):
        self.meta_title = content[:70]  # Set the first 70 characters of content as meta title
        self.meta_description = content[:160]  # Set the first 160 characters of content as meta description
        self.slug = slugify(content[:50])  # Generate slug from the first 50 characters of content
        return content