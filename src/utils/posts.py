import exceptions

def calculation_offset(page: int):
    """
    Calculation offset to db.
    Needs to pagination.
    """
    if page <= 0:
        raise exceptions.posts.PageLessZero
    return ((page * 10) - 10)