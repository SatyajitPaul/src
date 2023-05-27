from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.param_functions import Path

from database import get_db
from models import User, Follow
# from .schemas import FollowCreate
from .auth import get_user_from_token

router = APIRouter()

@router.post("/follow/{username}", status_code=status.HTTP_201_CREATED, tags=['Start Following'])
def follow_user(username: str = Path(..., min_length=1), db: Session = Depends(get_db), current_user: User = Depends(get_user_from_token)):
    # Check if the user is trying to follow themselves
    if current_user.username == username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")

    # Check if the user to follow exists in the database
    user_to_follow = db.query(User).filter(User.username == username).first()
    if not user_to_follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the follow relationship already exists
    existing_follow = db.query(Follow).filter(Follow.follower_id == current_user.id, Follow.following_id == user_to_follow.id).first()
    if existing_follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already following this user")

    # Create the follow relationship
    follow = Follow(follower_id=current_user.id, following_id=user_to_follow.id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    user_to_follow.followers_count += 1
    current_user.following_count += 1
    db.commit()

    return {"message": "You are now following the user"}

@router.delete("/unfollow/{username}", status_code=status.HTTP_204_NO_CONTENT, tags=['Stop Following'])
def unfollow_user(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_user_from_token)):
    # Check if the user to unfollow exists in the database
    user_to_unfollow = db.query(User).filter(User.username == username).first()
    if not user_to_unfollow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the follow relationship exists
    follow = db.query(Follow).filter(Follow.follower_id == current_user.id, Follow.following_id == user_to_unfollow.id).first()
    if not follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not following this user")

    # Delete the follow relationship
    db.delete(follow)
    db.commit()
    user_to_unfollow.followers_count -= 1
    current_user.following_count -= 1
    db.commit()

    return None
