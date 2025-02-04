from exceptions.base import Base

class PostsNotFound(Base):
    def __init__(self):
        super().__init__(404, "Posts not found 0_o!")

class PostNotFound(Base):
    def __init__(self):
        super().__init__(404, "Post not found 0_o!")

class ItsNotYour(Base):
    def __init__(self):
        super().__init__(400, "It's not your post •`_´•!")

class PageLessZero(Base):
    def __init__(self):
        super().__init__(400, "Page less zero!")