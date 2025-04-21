import os
import sys
from src.database.db_operations import Database, init_db, clear_database

# Import dm.py components directly
from src import dm

# Test database name
TEST_DB_NAME = "dnd_gm_test"

def before_all(context):
    """Set up test database and clear it before running tests"""
    # Store the db_name in the context for use in steps
    context.db_name = TEST_DB_NAME
    
    # Initialize the dm module's database with the test database name
    dm.initialize_db(TEST_DB_NAME)
    
    print(f"Test database '{TEST_DB_NAME}' initialized") 