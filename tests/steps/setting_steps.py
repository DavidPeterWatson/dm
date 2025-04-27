import json
from behave import given, when, then
from src.dm import (
    create_setting_tool,
    update_setting_tool,
    delete_setting_tool,
    search_settings_tool,
    filter_settings_by_type_tool,
    filter_settings_by_parent_tool,
    get_setting_by_name_tool,
    delete_all_settings_tool,
    list_settings_resource
)

import logging
logger = logging.getLogger('behave')

# Helper function to convert comma-separated strings to lists for list fields
def process_setting_fields(setting_data):
    list_fields = [
        'distinctive_features',
        'key_locations',
        'points_of_interest',
        'travel_routes',
        'factions',
        'encounter_recommendations',
        'dramatic_element_opportunities'
    ]
    
    # Convert comma-separated strings to lists for list fields
    for field in list_fields:
        if field in setting_data and isinstance(setting_data[field], str):
            setting_data[field] = [item.strip() for item in setting_data[field].split(',')]
    
    return setting_data

@given('there are no settings')
def step_impl_no_settings(context):
    # Clear all settings from the database
    delete_all_settings_tool()

@given('a setting "{name}" exists')
def step_impl_setting_exists(context, name):
    # First make sure there are no duplicate settings
    delete_all_settings_tool()
    
    # Create a basic setting for testing
    setting_data = {
        'setting_type': 'City',
        'name': name,
        'region': 'Test Region',
        'scale': 'Medium',
        'population': 'Test population',
        'distinctive_features': ['Feature 1', 'Feature 2']  # Provide as a list
    }
    setting = create_setting_tool(**setting_data)
    context.created_setting = setting

@when('I create a setting with the following details')
def step_impl_create_setting_details(context):
    setting_data = {}
    for row in context.table:
        field = row['field']
        value = row['value']
        
        # Handle placeholder for parent_id
        if field == 'parent_id' and value.startswith('{') and value.endswith('}'):
            # Extract the setting name from the placeholder
            parent_name = value[1:-1].split("'")[0]  # Extract name from {Name's ID}
            # Search for parent setting by name
            search_results = search_settings_tool(query=parent_name)
            parent_settings = [s for s in search_results["settings"] if s.name == parent_name]
            if parent_settings:
                value = parent_settings[0].id
            else:
                raise ValueError(f"Parent setting {parent_name} not found")
        
        setting_data[field] = value
    
    # Process list fields
    setting_data = process_setting_fields(setting_data)
    
    setting = create_setting_tool(**setting_data)
    context.created_setting = setting

@when('I create a setting with all details')
def step_impl_create_setting_all_details(context):
    setting_data = {}
    for row in context.table:
        setting_data[row['field']] = row['value']
    
    # Process list fields
    setting_data = process_setting_fields(setting_data)
    
    setting = create_setting_tool(**setting_data)
    context.created_setting = setting

@when('I create a setting named "{name}" of type "{setting_type}"')
def step_create_setting(context, name, setting_type):
    try:
        setting_data = {
            'name': name,
            'setting_type': setting_type,
            'region': 'Test Region',
            'scale': 'Medium',  # Add required field
            'population': '1000' # Add required field
        }
        context.created_setting = create_setting_tool(**setting_data)
        context.setting_name_already_exists_error = None
    except ValueError as e:
        context.setting_name_already_exists_error = str(e)
        context.created_setting = None

@when('I update the setting with the following details')
def step_impl_update_setting_details(context):
    setting = context.created_setting
    update_data = {'setting_id': setting.id}
    for row in context.table:
        update_data[row['field']] = row['value']
    # Process list fields
    update_data = process_setting_fields(update_data)
    result = update_setting_tool(**update_data)
    if isinstance(result, dict) and 'setting' in result:
        context.updated_setting = result['setting']
        context.warning_message = result.get('warning')
    else:
        context.updated_setting = result

@when('I update the setting with the following JSON')
def step_impl_update_setting_with_json(context):
    setting = getattr(context, 'created_setting', None)
    if not setting:
        # If not present, create a default setting for error scenarios
        setting_data = {
            'setting_type': 'City',
            'name': 'TestCity',
            'region': 'Test Region',
            'scale': 'Medium',
            'population': 'Test population',
            'distinctive_features': ['Feature 1', 'Feature 2']
        }
        setting = create_setting_tool(**setting_data)
        context.created_setting = setting
    try:
        import json
        update_data = json.loads(context.text)
        context.original_update_data = update_data.copy()
        update_data['setting_id'] = setting.id
        result = update_setting_tool(**update_data)
        if isinstance(result, dict) and 'setting' in result:
            context.updated_setting = result['setting']
            context.warning_message = result.get('warning')
            context.error_message = None
        else:
            context.updated_setting = result
            context.warning_message = None
            context.error_message = None
    except json.JSONDecodeError as e:
        context.error_message = str(e)
        context.updated_setting = None
        context.warning_message = None
    except (TypeError, ValueError) as e:
        context.error_message = str(e)
        context.updated_setting = None
        context.warning_message = None

@when('I delete the setting "{name}"')
def step_impl_delete_setting(context, name):
    try:
        # Get the setting by name
        setting = get_setting_by_name_tool(name=name)
        result = delete_setting_tool(setting_id=setting.id)
        context.delete_result = result
        context.deleted_setting_name = name
    except ValueError:
        context.delete_result = False
        context.deleted_setting_name = name

@when('I search for settings containing "{query}"')
def step_impl_search_settings(context, query):
    search_results = search_settings_tool(query=query)
    context.search_results = search_results["settings"]

@when('I search for settings of type "{setting_type}"')
def step_impl_filter_settings_by_type(context, setting_type):
    filtered_results = filter_settings_by_type_tool(setting_type=setting_type)
    context.search_results = filtered_results["settings"]

@when('I list all settings')
def step_impl_list_all_settings(context):
    # Import the function directly to access the resource
    all_settings = list_settings_resource()
    context.settings_list = all_settings["settings"]
    context.settings_response = all_settings

@given('the following settings exist')
def step_impl_multiple_settings_exist(context):
    # First make sure there are no duplicate settings
    delete_all_settings_tool()
    
    context.setting_ids = []
    for row in context.table:
        # Create a dictionary from the row with proper column names
        setting_data = {
            'name': row['name'],
            'setting_type': row['setting_type'],
            'region': row['region'],
            'scale': 'Medium',  # Add required field
            'population': '1000'  # Add required field
        }
        setting = create_setting_tool(**setting_data)
        context.setting_ids.append(setting.id)

@then('the setting "{name}" should be created successfully')
def step_impl_setting_created(context, name):
    try:
        setting = get_setting_by_name_tool(name=name)
        assert setting is not None
        assert setting.name == name
    except ValueError:
        assert False, f"Setting {name} was not found"

@then('the setting should have the following details')
def step_impl_check_setting_details(context):
    setting = context.created_setting
    for row in context.table:
        field = row['field']
        expected_value = row['value']
        actual_value = getattr(setting, field, None)
        # Convert lists to comma-separated strings for comparison
        if isinstance(actual_value, list):
            actual_value = ', '.join(actual_value)
        assert str(actual_value) == expected_value, f"Field '{field}' expected '{expected_value}', got '{actual_value}'"

@then('the setting "{name}" should be updated successfully')
def step_impl_setting_updated(context, name):
    try:
        setting = get_setting_by_name_tool(name=name)
        assert setting is not None
        assert setting.id == context.updated_setting.id
        assert setting.name == name
    except ValueError:
        assert False, f"Setting {name} was not found after update"

@then('the setting should have the updated fields')
def step_impl_check_updated_setting_details(context):
    setting = context.updated_setting
    for row in context.table:
        field = row['field']
        expected_value = row['value']
        actual_value = getattr(setting, field, None)
        # Convert lists to comma-separated strings for comparison
        if isinstance(actual_value, list):
            actual_value = ', '.join(actual_value)
        assert str(actual_value) == expected_value, f"Field '{field}' expected '{expected_value}', got '{actual_value}'"

@then('the setting "{name}" should be deleted successfully')
def step_impl_setting_deleted(context, name):
    try:
        setting = get_setting_by_name_tool(name=name)
        assert False, f"Setting {name} was found after deletion"
    except ValueError:
        # Expected behavior - setting not found
        pass

@then('the setting "{name}" should no longer be in the list of settings')
def step_impl_setting_not_in_list(context, name):
    all_settings = search_settings_tool(query="")
    setting_names = [setting.name for setting in all_settings["settings"]]
    assert name not in setting_names

@then('the setting search results should include "{name}"')
def step_impl_search_include(context, name):
    setting_names = [setting.name for setting in context.search_results]
    assert name in setting_names, f"Setting {name} not found in search results: {setting_names}"

@then('the setting search results should not include "{name}"')
def step_impl_search_exclude(context, name):
    setting_names = [setting.name for setting in context.search_results]
    assert name not in setting_names, f"Setting {name} should not be in search results: {setting_names}"

@then('I should see an error that the setting name already exists')
def step_setting_name_exists_error(context):
    assert context.setting_name_already_exists_error is not None
    assert "already exists" in context.setting_name_already_exists_error 

@then('the settings list should be empty')
def step_impl_settings_list_empty(context):
    assert len(context.settings_list) == 0, f"Expected empty list but got {len(context.settings_list)} settings"

@then('I should receive a message indicating no settings exist')
def step_impl_check_no_settings_message(context):
    assert context.settings_response["message"] == "No settings found. Use the create_setting_tool to add new settings."
    assert context.settings_response["count"] == 0 

@given('the following hierarchical settings exist')
def step_impl_hierarchical_settings_exist(context):
    # First make sure there are no duplicate settings
    delete_all_settings_tool()
    
    context.setting_ids = {}
    
    # First pass: Create all settings without parent relationships
    for row in context.table:
        setting_data = {
            'name': row['name'],
            'setting_type': row['setting_type'],
            'region': 'Test Region',  # Default value
            'scale': 'Medium',        # Required field
            'population': '1000'      # Required field
        }
        setting = create_setting_tool(**setting_data)
        context.setting_ids[row['name']] = setting.id
    
    # Second pass: Update settings with parent relationships
    for row in context.table:
        if row['parent'] != 'None':
            parent_id = context.setting_ids[row['parent']]
            update_setting_tool(setting_id=context.setting_ids[row['name']], parent_id=parent_id)

@when('I filter settings to show children of "{parent_name}"')
def step_impl_filter_settings_by_parent(context, parent_name):
    # Search for the parent setting by name
    search_results = search_settings_tool(query=parent_name)
    parent_setting = next((s for s in search_results["settings"] if s.name == parent_name), None)
    
    if parent_setting:
        # Use the new tool to filter settings by parent ID
        filtered_results = filter_settings_by_parent_tool(parent_id=parent_setting.id)
        context.search_results = filtered_results["settings"]
    else:
        context.search_results = []

@then('I should see an error about invalid JSON format')
def step_impl_check_invalid_json_error(context):
    assert context.error_message is not None, "Expected an error message but none was set"
    # The exact error message can vary, but it should indicate a JSON parsing problem
    assert any(term in context.error_message for term in 
              ["JSON", "json", "Unterminated", "Invalid control character", "Expecting", "line", "column"]), \
        f"Expected JSON error but got: {context.error_message}"

@then('I should see an error about invalid field types')
def step_impl_check_invalid_field_type_error(context):
    assert context.error_message is not None
    assert "type" in context.error_message.lower()

@then('the setting should be updated with valid fields only')
def step_impl_check_valid_fields_updated(context):
    # Check that only valid fields were updated
    setting = context.updated_setting
    valid_fields = [field for field in context.original_update_data.keys() 
                   if hasattr(setting, field)]
    
    # If there are no valid fields, we just verify that the setting exists
    if not valid_fields:
        assert setting is not None, "Setting should exist even with no valid fields"
        return
    
    for field in valid_fields:
        expected_value = context.original_update_data[field]
        actual_value = getattr(setting, field)
        assert str(actual_value) == str(expected_value), f"Field {field} not updated correctly"

@then('the setting "{child_name}" should have "{parent_name}" as its parent setting')
def step_impl_check_setting_parent(context, child_name, parent_name):
    try:
        child_setting = get_setting_by_name_tool(name=child_name)
        parent_setting = get_setting_by_name_tool(name=parent_name)
        
        assert child_setting.parent_id == parent_setting.id, f"Setting {child_name} does not have {parent_name} as parent"
    except ValueError as e:
        assert False, str(e)

@then('the setting "{parent_name}" should have "{child_name}" as a child setting')
def step_impl_check_setting_child(context, parent_name, child_name):
    try:
        parent_setting = get_setting_by_name_tool(name=parent_name)
        child_setting = get_setting_by_name_tool(name=child_name)
        
        # Check if the child has the parent's ID as parent_id
        assert child_setting.parent_id == parent_setting.id, f"Setting {child_name} does not have {parent_name} as parent"
    except ValueError as e:
        assert False, str(e)

@then('I should see a warning: "{warning_text}"')
def step_impl_check_explicit_warning_text(context, warning_text):
    assert hasattr(context, 'warning_message'), "Context should have a warning_message attribute"
    assert context.warning_message is not None, "Warning message should not be None"
    assert context.warning_message == warning_text, f"Expected warning '{warning_text}' but got: '{context.warning_message}'" 