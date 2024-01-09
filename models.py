from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id  # Unique user identifier, usually retrieves the user's ID from the database
