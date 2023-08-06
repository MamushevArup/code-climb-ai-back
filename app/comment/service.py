from app.config import database
from .repository.repository import CommentRepository

class Service:
    def __init__(
            self, 
            repository: CommentRepository
    ):
        self.repository = repository

def get_service():
    repository = CommentRepository(database)
    return Service(repository)