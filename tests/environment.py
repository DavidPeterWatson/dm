from src.database.db_operations import init_db, clear_database

# Test database name
TEST_DB_NAME = "dnd_gm_test"

def before_all(context):
    """Set up test database and clear it before running tests"""
    # Initialize with test database
    init_db(TEST_DB_NAME)
    clear_database()
    print(f"Test database '{TEST_DB_NAME}' initialized and cleared") 