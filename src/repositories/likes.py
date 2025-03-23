from repositories.alchemy_repo import SQLAlchemyRepository
from models.models import PostsLikesModel

class LikesRepository(SQLAlchemyRepository):
    model = PostsLikesModel