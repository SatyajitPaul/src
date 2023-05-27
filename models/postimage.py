from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from PIL import Image as PILImage
from datetime import datetime


from database import Base

#This will store image related to post
class PostImage(Base):
    __tablename__ = "images"

    id = mapped_column(Integer, primary_key=True, index=True)
    url = mapped_column(String)
    caption = mapped_column(String)
    post_id = mapped_column(Integer, ForeignKey("posts.id"))
    created_at = mapped_column(DateTime, default=datetime.now())

    post = relationship("Post", back_populates="images")

    def open_image(self) -> PILImage.Image:
        return PILImage.open(self.file_path)