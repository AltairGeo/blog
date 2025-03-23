import exceptions
from typing import List, Dict
from models.models import PostsLikesModel


def calculation_offset(page: int):
    """
    Calculation offset to db.
    Needs to pagination.
    """
    if page <= 0:
        raise exceptions.posts.PageLessZero
    return ((page * 10) - 10)


def calc_likes_and_dislikes(likes_list: List[PostsLikesModel]) -> Dict[str, int]:
    likes = sum(1 for like in likes_list if like.is_like)
    dislikes = sum(1 for like in likes_list if not like.is_like)
    return {"likes": likes, "dislikes": dislikes}