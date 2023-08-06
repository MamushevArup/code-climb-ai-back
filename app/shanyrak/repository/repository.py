from typing import Any, Optional
from bson import ObjectId
from pymongo.database import Database

class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database
    def create_post_shanyraq(self, user_id: str,shan: dict[str, Any], collection_name:str) -> Optional[dict[str, Any]]:
        shan["user_id"] = ObjectId(user_id)
        sh = self.database[collection_name].insert_one(shan)
        return sh.inserted_id
    
    def get_shanyrak_by_id(self,  id : str, collection_name:str) -> dict[str, Any]:
        return self.database[collection_name].find_one({"_id": ObjectId(id)})
    
    def update_shanyrak(self, id : str, inp : dict, jwt_id: str):
        filter = {"_id" : ObjectId(id), "user_id" : ObjectId(jwt_id)}
        update = {"$set" : inp}
        self.database["shanyraq"].update_one(filter, update)

    def delete_shanyrak(self, id : str, jwt_id : str, collection_name:str):
        filter = {"_id" : ObjectId(id), "user_id": ObjectId(jwt_id)}
        self.database[collection_name].delete_one(filter)

    def add_image_shanyrak(self, house_id : str, media : list):
        filter = {"_id" : ObjectId(house_id)}
        update = {"$push" : {"media" : media}}
        self.database["shanyraq"].insert_one({"image" :media})

    def delete_media(self, house_id:str):
        filter = {"_id":ObjectId(house_id)}
        update = {"$unset":{"media": 1}}
        self.database["shanyraq"].update_one(filter, update)
        
    def show_option(self, house_id:str) -> dict[str, list]:
        return self.database["shanyraq"].find_one({"_id": ObjectId(house_id)}, {"_id": 0, "media":1})
    
    def upload_avatar(self, user_id, image : str):
        filter = {"_id" : ObjectId(user_id)}
        up = {"$set" : {"avatar_url" : image}}
        self.database["user"].update_one(filter, up)
    
    def delete_avatar(self, user_id : str):
        self.database["users"].update_one({"_id":ObjectId(user_id)}, {"$unset" : {"avatar_url" : 1}})
    
    def return_ava(self, user_id):
        return self.database["users"].find_one({"_id": ObjectId(user_id)}, {"avatar_url" : 1})

    def pagination(self, limit : int, offset : int, type:str, rooms_count:int, price_from:int, price_until:int):
        query = {}
        if type is not None:
            query["type"] = type
        if rooms_count is not None:
            query["rooms_count"] = rooms_count
        if price_from is not None and price_until is not None:
            query["price"] = {
            "$gt": price_from,
            "$lt": price_until
        }

        collection_count = self.database["shanyraq"].count_documents(query)
        res = self.database["shanyraq"].find(query).limit(limit).skip(offset).sort([("created_at", 1)])
        arr = []
        for r in res:
            arr.append(r)
        return {
            "total":collection_count,
            "objects":arr   
        }
    
    def review_houses(self,limit:int, offset:int):
        collection_count = self.database["waitlist"].count_documents({})
        res = self.database["waitlist"].find({}).limit(limit).skip(offset).sort([("created_at", 1)])
        arr = []
        for r in res:
            arr.append(r)
        return {
            "total":collection_count,
            "objects":arr   
        }
    def delete_for_moderators(self, house_id:str):
        self.database["waitlist"].delete_one({"_id":ObjectId(house_id)})

    def get_lang(self, email : str):
        val = self.database["user"].find_one({"email" : email}, {"_id":0})
        return val
    
    def create_user_db(self, payload:dict):
        self.database["user"].insert_one(payload)

    def get_user_by_email_db(self, email:str):
        return self.database["user"].find_one({"email":email})
    
    def update_one_db(self, user_id : str, last_login:str):
        update_object = {
            '$set': {
            'created_at': last_login,
            },
        }
        self.database["user"].update_one({"user_id":user_id}, update_object)

    