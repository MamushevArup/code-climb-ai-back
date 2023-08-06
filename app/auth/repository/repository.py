from datetime import datetime
from typing import  Optional

from bson import ObjectId
from pymongo.database import Database
import string
import random   

class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, email:str, username:str, image_url:str):
        characters = string.ascii_letters + string.digits
        hash = ''.join(random.choice(characters) for _ in range(16))
        payload = {
            "email": email,
            "username":username,
            "image_url" : image_url,
            "last_login":datetime.now(),
            "profile_id" : hash
        }

        return self.database["users"].insert_one(payload)
    
    def get_hash(self, user_id):
        p_id = self.database["users"].find_one({"_id" : ObjectId(user_id)}, {"profile_id" : 1, "_id" : 0})
        return p_id
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user
    
    def update_user_by_email(self, email : str):
        filter = {
            "email" : email
        }
        update = {
            "$set" : {
                "last_login" : datetime.now()
            }
        }
        self.database["users"].update_one(filter, update)

    def update_user_lang_db(self, id:str,new_grade:str, new_direct:str, new_selected_language:str, new_selected_frameworks:str, new_selected_technologies:str):
        filter = {"_id" : ObjectId(id)}
        update = { "$set": {
            "grade": new_grade,
            "direct": new_direct,
            "selectedLanguage": new_selected_language,
            "selectedFrameworks": new_selected_frameworks,
            "selectedTechnologies": new_selected_technologies,
        }}

        heap_all_tech = []
        heap_all_tech = [new_selected_language]
        for i in new_selected_frameworks:
            heap_all_tech.append(i)
        for i in new_selected_technologies:
            heap_all_tech.append(i)

        get_for_remove_dup = self.database["users"].find_one({"_id" : ObjectId(id)}, {"_id": 0, "all_technologies": 1})
        
        if get_for_remove_dup:
            for i in get_for_remove_dup["all_technologies"]:
                heap_all_tech.append(i)

        set_heap = list(set(heap_all_tech))
        push = {"$set": {
            "all_technologies":  set_heap,
        }}

        # Combine the update and push operations in a single dictionary

        self.database["users"].update_one(filter, update)
        self.database["users"].update_one(filter, push)
    
    def get_language_db(self, id:str):
        language = self.database["users"].find_one({"_id":ObjectId(id)}, {"_id" : 0, "last_login":0, "profile_id":0})
        return language
    
    def save_gpt_question(self, info:dict):
        id = self.database["questions"].insert_one(info | {"created_at" : datetime.now()})
        return id.inserted_id

    def update_gpt_right_answer(self, id : str, answer:str):
        filter = {"_id" : ObjectId(id)}
        update = {"$set" : { "right_answer" : answer}}
        self.database["questions"].update_one(filter, update)

    def add_list_question(self, id:str, list_question:list[str]):
        curr_time = datetime.now()
        insert = self.database["list_questions"].insert_one( {"user_id" : id} | {"list_questions" : list_question} | {"created_at" : curr_time}) 
        return insert.inserted_id

    def get_list_question(self, id: str):
        cursor = self.database["list_questions"].find({"user_id": id}).sort("created_at", -1).limit(1)
        documents = list(cursor)
        if documents:
            return documents[0]["list_questions"], documents[0]["_id"]
        return None
    
    def find_all_users_answer(self, list_id:str):
        return self.database["questions"].find({"list_question_id":list_id})
    
    def save_user_message_db(self, hmap:dict()):
        is_exist = self.database["saved_questions"].find_one({"user_id" : hmap.user_id}, {"_id" : 0, "saved_message" : 1})

        if is_exist is None :
            save = {"saved_message" : [hmap.saved_message]}
            create = self.database["saved_questions"].insert_one(hmap.dict()  | save | {"saved_at" : datetime.now()})
            return create.inserted_id

        set_str = set([hmap.saved_message])
        for i in is_exist["saved_message"]:
            if i in set_str:
                return True
            else:
                set_str.add(i)

        filter = {"user_id" : hmap.user_id}
        update_filter = {"$set" : {"saved_message" : list(set_str)}}
        update = self.database["saved_questions"].update_one(filter, update_filter)
        return update.upserted_id
    
    # When user choose stack he can choose the language and we collect how many times user choose this language
    # Ex js : 1, pyhton : 2, java : 3
    def technology_count(self, user_id:str, language:str):
        if language == '':
            return
        # We check if user choose this language before
        find = self.database["languages"].find_one({"user_id" : user_id, "language" : language}, {"_id" : 0, "count" : 1, "language" : 1})
        # If user choose this language before we update count + 1
        payload = {
            "user_id" : user_id,
            "language" : language,
            "count" : find["count"] + 1 if find else 1
        }
        # If we already have this language in the collection we update it or create new document instead.
        if find :
            update_collection = self.database["languages"].update_one({"user_id" : user_id, "language" : language}, {"$set" : {"count" : find["count"] + 1}})
            return update_collection.upserted_id
        new_collection = self.database["languages"].insert_one(payload)
        return new_collection.inserted_id
    
    # We need this function to get all languages that user choose before for our statistic and frontend part
    def get_technology_count(self, user_id:str):
        find = self.database["languages"].find({"user_id" : user_id}, {"_id":0, "user_id":0})
        return find
    
    def add_image_shanyrak(self, house_id : str, media : list):
        filter = {"_id" : ObjectId(house_id)}
        update = {"$push" : {"media" : media}}
        self.database["shanyraq"].insert_one({"image" :media})
    
    def upload_image_s3(self, id:str, image:str):
        filter = {"_id" : ObjectId(id)}
        update = {"$set" : {"image_url" : image}}
        self.database["users"].update_one(filter, update)
    
    def get_saved_db(self, id:str):
        return self.database["saved_questions"].find_one({"user_id" : id}, {"_id" : 0, "saved_message" : 1})
    
    def get_all_questions_from_interview(self, user_id:str):
        pipeline = [
            {
                "$match": {"user_id": user_id}
            },
            {
                "$group": {
                    "_id": "$list_question_id",
                    "questions": {
                        "$push": {
                            "question": "$question",
                            "user_answer": "$user_answer",
                            "right_answer": "$right_answer"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "questions": 1
                }
            }
        ]
        val = self.database["questions"].aggregate(pipeline)
        res = []
        for i in val :
            res.append(i)
        return res

