from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from typing import Optional, Dict, Any

# Default connection settings
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("DB_NAME", "dnd_gm")

# Initialize with None, will be set up in init_db
client = None
db = None
campaigns_collection = None
characters_collection = None

def init_db(db_name: Optional[str] = None):
    """Initialize database connection with optional database name override"""
    global client, db, campaigns_collection, characters_collection
    
    # Use provided db_name or fall back to default
    actual_db_name = db_name or DB_NAME
    
    client = MongoClient(MONGODB_URI)
    db = client[actual_db_name]
    campaigns_collection = db["campaigns"]
    characters_collection = db["characters"]
    return db

# Initialize with default settings
init_db()

# Helper function to convert between MongoDB ObjectId and integer ID
def objectid_to_int(oid):
    return int(str(oid)[-8:], 16)

# Helper function to convert MongoDB ObjectId to string
def objectid_to_str(oid):
    return str(oid)

def clear_database():
    """Clear all campaigns and characters from the database"""
    campaigns_collection.delete_many({})
    characters_collection.delete_many({})
    return True 