from behave import given, when, then
from src.dm import get_database_info_tool

@given('the database is initialized')
def step_given_database_initialized(context):
    # The database is already initialized in environment.py
    assert hasattr(context, 'db_name')

@when('I request the database info')
def step_when_request_database_info(context):
    context.db_info = get_database_info_tool()

@then('I should see the database name')
def step_then_see_database_name(context):
    assert 'name' in context.db_info
    assert context.db_info['name'] == context.db_name

@then('I should see the number of campaigns')
def step_then_see_campaign_count(context):
    assert 'campaign_count' in context.db_info
    assert isinstance(context.db_info['campaign_count'], int)

@then('I should see the number of characters')
def step_then_see_character_count(context):
    assert 'character_count' in context.db_info
    assert isinstance(context.db_info['character_count'], int)

@then('I should see the number of settings')
def step_then_see_setting_count(context):
    assert 'setting_count' in context.db_info
    assert isinstance(context.db_info['setting_count'], int) 