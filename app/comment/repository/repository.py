from bson import ObjectId
from pymongo.database import Database

class CommentRepository:
    def __init__(self, database : Database):
        self.database = database
    def create_comment_shanyrak(self, data: dict, house_id:str):
        data["house_id"] = ObjectId(house_id)
        self.database["comments"].insert_one(data)
    def get_comment_by_id(self, id : str):
        message = self.database["comments"].find({"house_id": ObjectId(id)})
        arr = []
        for m in message:
            arr.append(m)
        return arr
    def update_comment_by_id(self, house_id: str, comment_id: str, inp:dict):
        filter = {"house_id": ObjectId(house_id), "_id": ObjectId(comment_id)}
        second_filter = {"$set": {"content" : inp["content"]}}
        self.database["comments"].update_one(filter, second_filter)
    def delete_comment(self, house_id: str, comment_id: str):
        filter = {"house_id": ObjectId(house_id), "_id": ObjectId(comment_id)}
        self.database["comments"].delete_one(filter)