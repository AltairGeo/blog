from repositories.alchemy_repo import SQLAlchemyRepository
from models.posts import PostsModel

class PostsRepository(SQLAlchemyRepository):
    model = PostsModel

