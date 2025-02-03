from fastapi import HTTPException

class Base(HTTPException):
    def __init__(self, status_code, detail = None, headers = None):
        super().__init__(status_code, detail, headers)


class SomethingWasWrong(Base):
    def __init__(self):
        super().__init__(400, "Something was wrong!")