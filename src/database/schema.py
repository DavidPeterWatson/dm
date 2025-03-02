from pymongo import MongoClient

def initialize_database(mongodb_uri: str = "mongodb://localhost:27017/", db_name: str = "dnd_gm"):
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    
    # Set up campaigns collection
    campaigns_collection = db["campaigns"]
    campaigns_collection.create_index("name")
    campaigns_collection.create_index("description")
    
    # Set up characters collection
    characters_collection = db["characters"]
    characters_collection.create_index("name")
    characters_collection.create_index("campaign_id")
    characters_collection.create_index("class")
    characters_collection.create_index("race")

    print("MongoDB initialized successfully.")

if __name__ == "__main__":
    initialize_database() 
