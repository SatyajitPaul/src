from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
from enum import Enum as PyEnum
from typing import List
from schemas import PostCreate
from database import get_db
from models import Post, User, PostImage
from PIL import Image

from .auth import get_user_from_token



router = APIRouter(prefix="/post")

#API route for creating new post for logged in user, a post can have content of 1024 words and it can multiple images, also we capture the time of the post creation, also post will contain a boolean flag is anonymous which will be false by default, also we will get the privacy type from the user
@router.post("/create", tags=['Create Post'])
async def createPost(postData: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_user_from_token)):
    # Check if the user is logged in
    # if not current_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="You must be logged in to create a post"
    #     )
    # # Create the post
    # user = current_user
    post = Post(content=postData.content, is_anonymous=postData.is_anonymous,
                privacy_type=postData.privacy_type, user_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    # imageLimit: Integer = 1
    # for image_data in postImage:
    #     savedImage = save_image(image_data)
    #     image = PostImage(url=savedImage, caption="Post Image")
    #     post.images.append(image)

    # Update the post count for the user
    current_user.post_count += 1
    db.commit()

    # Upload and associate the images with the post
    # for image in postData.images:
    #     image_path = save_image(image)
    #     post.images.append(Image(file_path=image_path))
    # db.commit()

    return {"message": "Post created successfully"}


# @router.get("/current_user_id")
# def get_current_user_id(current_user: User = Depends(get_user_from_token)):
#     print("$$$$$$$$$$$$$$$$$")
#     print(current_user)
#     if not current_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged in")
#     return {"user_id": current_user.id}