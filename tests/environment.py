from src.database.db_operations import Database, init_db, clear_database

# Test database name
TEST_DB_NAME = "dnd_gm_test"

def before_all(context):
    """Set up test database and clear it before running tests"""
    context.db = Database()
    init_db(context.db, None, TEST_DB_NAME)
    clear_database(context.db)
    print(f"Test database '{TEST_DB_NAME}' initialized and cleared") 