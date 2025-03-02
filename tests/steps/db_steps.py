from behave import given, when, then
from src.database.db_operations import clear_database

@given('the D&D GM Assistant is running')
def step_impl_start_server(context):
    # In a real scenario, you would start the server here
    pass

@given('an empty database')
def step_impl_empty_database(context):
    clear_database()