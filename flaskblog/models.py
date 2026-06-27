from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from flask_login import UserMixin

@dataclass
class User(UserMixin):
    id: int
    username: str
    email: str
    password: str
    image_file: str = 'img/default.jpg'
    posts: List['Post'] = field(default_factory=list)

    def __init__(self, user_id, username, email, password, image_file='default.jpg', **kwargs):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.image_file = image_file if image_file else 'img/default.jpg'

@dataclass
class Post:
    id: int
    title: str
    content: str
    date_posted: datetime
    user_id: int

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.date_posted = datetime.now()
        self.user_id = user_id
