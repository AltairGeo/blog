class UserAlreadyCreate(Exception):
    def __init__(self):
        super().__init__("User has already been created!")
        self.status_code = 400

class UserNotFound(Exception):
    def __init__(self):
        super().__init__("User not found!")
        self.status_code = 404