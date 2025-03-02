from behave import given, when, then
from src.database.character_operations import (
    create_character, get_character, list_characters,
    delete_character, update_character, search_characters, update_character_progress, get_character_by_name
)
from src.database.campaign_operations import create_campaign, get_campaign_by_name
from src.models.character import Character
import json

@given('a character "{name}" exists for "{campaign_name}" campaign')
def step_impl_character_exists(context, name, campaign_name):
    # Create the character
    campaign = get_campaign_by_name(campaign_name)
    character = create_character(
        name=name,
        campaign_id=campaign.id,
        player_name="Test Player",
        race="Human",
        character_class="Fighter",
        level=1
    )
    context.character_id = character.id

@when('I create a character with the following details')
def step_impl_create_character_details(context):
    table = context.table
    for row in table:
        name = row['name']
        race = row['race']
        character_class = row['class']
        campaign_name = row['campaign_name']
        campaign = get_campaign_by_name(campaign_name)
        
        character = create_character(
            name=name,
            campaign_id=campaign.id,
            race=race,
            character_class=character_class
        )
        context.created_character = character
        context.character_id = character.id

@when('I update the character with the following details')
def step_impl_update_character_details(context):
    table = context.table
    update_data = {}
    
    for row in table:
        for column in row.headings:
            if column.startswith('ability_scores.'):
                # Handle nested ability scores
                ability = column.split('.')[1]
                if 'ability_scores' not in update_data:
                    update_data['ability_scores'] = {}
                update_data['ability_scores'][ability] = int(row[column])
            else:
                # Handle regular fields
                update_data[column] = int(row[column]) if row[column].isdigit() else row[column]
    
    updated_character = update_character(context.character_id, **update_data)
    context.updated_character = updated_character

@when('I delete the character "{name}"')
def step_impl_delete_character(context, name):
    result = delete_character(context.character_id)
    context.delete_result = result
    context.deleted_character_name = name

@when('I search for characters with class "{character_class}"')
def step_impl_search_characters_by_class(context, character_class):
    context.search_results = search_characters(character_class=character_class)

@when('I update the character\'s campaign progress with')
def step_impl_update_character_progress(context):
    table = context.table
    for row in table:
        current_location = row['current_location']
        key_discoveries = [row['key_discoveries']]
        
        updated_character = update_character_progress(
            context.character_id,
            current_location=current_location,
            key_discoveries=key_discoveries
        )
        context.updated_character = updated_character

@then('the character "{name}" should be created successfully')
def step_impl_character_created(context, name):
    character = get_character(context.created_character.id)
    assert character.name == name

@then('{name} should be associated with the "{campaign_name}" campaign')
def step_impl_character_associated_with_campaign(context, name, campaign_name):
    campaign = get_campaign_by_name(campaign_name)
    character = get_character_by_name(name, campaign.id)
    assert character.campaign_id == campaign.id

@then('the character "{name}" should be updated successfully')
def step_impl_character_updated(context, name):
    character = get_character(context.character_id)
    assert character.name == name

@then('the character\'s level should be {level:d}')
def step_impl_character_level(context, level):
    character = get_character(context.character_id)
    assert character.level == level

@then('the character\'s intelligence score should be {score:d}')
def step_impl_character_intelligence(context, score):
    character = get_character(context.character_id)
    assert character.data.get('ability_scores', {}).get('intelligence') == score

@then('the character "{name}" should be deleted successfully')
def step_impl_character_deleted(context, name):
    assert context.delete_result is True
    
    try:
        get_character(context.character_id)
        assert False, "Character was not deleted - still retrievable by ID"
    except ValueError:
        # This is the expected path - character should not be found
        pass

@then('the character should no longer be in the list of characters')
def step_impl_character_not_in_list(context):
    characters = list_characters()
    character_names = [character.name for character in characters]
    assert context.deleted_character_name not in character_names

@then('the character search results should include "{name}"')
def step_impl_search_include_character(context, name):
    character_names = [character.name for character in context.search_results]
    assert name in character_names

@then('the character search results should not include "{name}"')
def step_impl_search_exclude_character(context, name):
    character_names = [character.name for character in context.search_results]
    assert name not in character_names

@given('the following characters exist')
def step_impl_multiple_characters_exist(context):
    # Make sure we have campaigns for these characters
    if not hasattr(context, 'campaign_ids'):
        # Create two campaigns
        campaign1 = create_campaign("Campaign 1", "First test campaign")
        campaign2 = create_campaign("Campaign 2", "Second test campaign")
        context.campaign_ids = [campaign1.id, campaign2.id]
    
    context.character_ids = []
    for row in context.table:
        name = row['name']
        race = row['race']
        character_class = row['class']
        campaign_name = row['campaign_name']
        campaign = get_campaign_by_name(campaign_name)
        
        character = create_character(
            name=name,
            campaign_id=campaign.id,
            race=race,
            character_class=character_class
        )
        context.character_ids.append(character.id)

@then('the character\'s campaign progress should be updated successfully')
def step_impl_character_progress_updated(context):
    character = get_character(context.character_id)
    assert 'campaign_progress' in character.data

@then('the character\'s current location should be "{location}"')
def step_impl_character_location(context, location):
    character = get_character(context.character_id)
    assert character.data.get('campaign_progress', {}).get('current_location') == location 