from pymongo import MongoClient
import os
from typing import Optional

# Default connection settings
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("DB_NAME", "dnd_gm")

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.campaigns_collection = None
        self.characters_collection = None
        self.settings_collection = None  # Added settings collection
        # Add other collections as needed
        self.initialized = False
    
def init_db(db: Database, connection_string: Optional[str] = None, db_name: Optional[str] = None):
    """Initialize the database connection and collections"""
    if db.initialized:
        return
        
    # Default connection values
    connection_string = connection_string or MONGODB_URI
    db_name = db_name or DB_NAME
    
    db.client = MongoClient(connection_string)
    db.db = db.client[db_name]
    
    # Set up campaigns collection
    db.campaigns_collection = db.db.campaigns
    db.campaigns_collection.create_index("name")
    db.campaigns_collection.create_index("description")
    
    # Set up characters collection
    db.characters_collection = db.db.characters
    db.characters_collection.create_index("name")
    db.characters_collection.create_index("campaign_id")
    db.characters_collection.create_index("class")
    db.characters_collection.create_index("race")

    # Set up settings collection
    db.settings_collection = db.db.settings
    db.settings_collection.create_index("name")
    db.settings_collection.create_index("setting_type")
    db.settings_collection.create_index("region")

    db.initialized = True

def close(db: Database):
    """Close the database connection"""
    if db.client:
        db.client.close()
        db.initialized = False

def clear_database(db: Database):
    """Clear all campaigns and characters from the database"""
    if not db.initialized:
        raise RuntimeError("Database not initialized. Call init_db() first.")
        
    db.campaigns_collection.delete_many({})
    db.characters_collection.delete_many({})
    db.settings_collection.delete_many({})  # Added settings collection
    return True

# Helper function to convert between MongoDB ObjectId and integer ID
def objectid_to_int(oid):
    return int(str(oid)[-8:], 16)

# Helper function to convert MongoDB ObjectId to string
def objectid_to_str(oid):
    return str(oid)

