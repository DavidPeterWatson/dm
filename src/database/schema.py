from pymongo import MongoClient

def initialize_database(mongodb_uri: str = "mongodb://localhost:27017/", db_name: str = "dnd_gm"):
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    campaigns_collection = db["campaigns"]

    # Create indexes if necessary
    campaigns_collection.create_index("name")
    campaigns_collection.create_index("description")

    print("MongoDB initialized successfully.")

if __name__ == "__main__":
    initialize_database() 
