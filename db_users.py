from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)

db = client['gh_coffee_db']


def check_and_add_user(message):
    if db.users.find_one({'user_id': message.from_user.id}) == None:
        new_user = {
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'user_id': message.from_user.id,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'старт'
        }
        db.users.insert_one(new_user)
    return

def get_current_state(user_id):
    user = db.users.find_one({'user_id':user_id})
    return user['state']


def set_state(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {"$set": {'state': state_value}})