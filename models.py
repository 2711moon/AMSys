from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['asset_management']

users_collection = db['users']
assets_collection = db['assets']
asset_types_collection = db['asset_types']