from behave import given, when, then
from src.dm import (
    create_character_tool,
    update_character_tool,
    delete_character_tool,
    search_characters_tool,
    get_character_resource,
    list_characters_resource,
    create_campaign_tool,
    search_campaigns_tool
)
from src.models.character import Character, Ability, Proficiencies, Personality, Spells, Familiar
import json

@given('a character "{name}" exists for "{campaign_name}" campaign')
def step_impl_character_exists(context, name, campaign_name):
    # Find campaign by name first
    campaigns = search_campaigns_tool(query=campaign_name)
    campaign = next((c for c in campaigns if c.name == campaign_name), None)
    
    # Check if character already exists for this campaign
    characters = search_characters_tool(query=name, campaign_id=campaign.id)
    print(f"DEBUG: Characters found for name '{name}' and campaign_id '{campaign.id}': {[{'name': c.name, 'campaign_id': c.campaign_id} for c in characters]}")
    character = next((c for c in characters if c.name == name and c.campaign_id == campaign.id), None)
    if character is None:
        # Create the character using the tool
        created_character = create_character_tool(
            name=name,
            campaign_id=campaign.id
        )
        context.character_id = created_character.id
    else:
        context.character_id = character.id

@when('I create a character with the following details')
def step_impl_create_character_details(context):
    table = context.table
    for row in table:
        name = row['name']
        race = row['race']
        character_class = row['class']
        campaign_name = row['campaign_name']
        
        # Find campaign by name first
        campaigns = search_campaigns_tool(query=campaign_name)
        campaign = next((c for c in campaigns if c.name == campaign_name), None)
        
        # Check if character already exists for this campaign
        characters = search_characters_tool(query=name, campaign_id=campaign.id)
        print(f"DEBUG: Characters found for name '{name}' and campaign_id '{campaign.id}': {[{'name': c.name, 'campaign_id': c.campaign_id} for c in characters]}")
        character = next((c for c in characters if c.name == name and c.campaign_id == campaign.id), None)
        if character is None:
            # Create the character using the tool
            created_character = create_character_tool(
                name=name,
                campaign_id=campaign.id,
                race=race,
                character_class=character_class
            )
            context.created_character = created_character
            context.character_id = created_character.id
        else:
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
    
    updated_character = update_character_tool(character_id=context.character_id, **update_data)
    context.updated_character = updated_character

@when('I delete the character "{name}"')
def step_impl_delete_character(context, name):
    result = delete_character_tool(character_id=context.character_id)
    context.delete_result = result
    context.deleted_character_name = name

@when('I search for characters with class "{character_class}"')
def step_impl_search_characters_by_class(context, character_class):
    context.class_search_results = search_characters_tool(character_class=character_class)

@then('the character "{name}" should be created successfully')
def step_impl_character_created(context, name):
    # Search for character by name
    characters = search_characters_tool(query=name)
    character = next((c for c in characters if c.name == name), None)
    assert character is not None
    assert character.name == name

@then('{name} should be associated with the "{campaign_name}" campaign')
def step_impl_character_associated_with_campaign(context, name, campaign_name):
    # Find campaign by name first
    campaigns = search_campaigns_tool(query=campaign_name)
    campaign = next((c for c in campaigns if c.name == campaign_name), None)
    
    # Find character by name
    characters = search_characters_tool(query=name)
    character = next((c for c in characters if c.name == name), None)
    
    assert character.campaign_id == campaign.id

@then('the character "{name}" should be updated successfully')
def step_impl_character_updated(context, name):
    character = get_character_resource(character_id=context.character_id)
    assert character.name == name

@then('the character\'s level should be {level:d}')
def step_impl_character_level(context, level):
    character = get_character_resource(character_id=context.character_id)
    assert character.level == level

@then('the character\'s {ability_score} score should be {score:d}')
def step_impl_character_ability_score(context, ability_score, score):
    character = get_character_resource(character_id=context.character_id)
    assert getattr(character.ability_scores, ability_score.lower()) == score

@then('the character "{name}" should be deleted successfully')
def step_impl_character_deleted(context, name):
    assert context.delete_result is True
    
    try:
        get_character_resource(character_id=context.character_id)
        assert False, "Character was not deleted - still retrievable by ID"
    except ValueError:
        # This is the expected path - character should not be found
        pass

@then('the character should no longer be in the list of characters')
def step_impl_character_not_in_list(context):
    characters = list_characters_resource()
    character_names = [character.name for character in characters]
    assert context.deleted_character_name not in character_names

@then('the character search results should include "{name}"')
def step_impl_search_include_character(context, name):
    character_names = [character.name for character in context.search_results]
    assert name in character_names

@then('the character class search results should include "{name}"')
def step_impl_class_search_include_character(context, name):
    character_names = [character.name for character in context.class_search_results]
    assert name in character_names

@then('the character search results should not include "{name}"')
def step_impl_search_exclude_character(context, name):
    character_names = [character.name for character in context.search_results]
    assert name not in character_names

@then('the character class search results should not include "{name}"')
def step_impl_class_search_exclude_character(context, name):
    character_names = [character.name for character in context.class_search_results]
    assert name not in character_names

@given('the following characters exist')
def step_impl_multiple_characters_exist(context):
    # Make sure we have campaigns for these characters
    if not hasattr(context, 'campaign_ids'):
        # Create two campaigns
        campaign1 = create_campaign_tool(name="Campaign 1", description="First test campaign")
        campaign2 = create_campaign_tool(name="Campaign 2", description="Second test campaign")
        context.campaign_ids = [campaign1.id, campaign2.id]
    
    context.character_ids = []
    for row in context.table:
        name = row['name']
        race = row['race']
        character_class = row['class']
        campaign_name = row['campaign_name']
        
        # Find campaign by name first
        campaigns = search_campaigns_tool(query=campaign_name)
        campaign = next((c for c in campaigns if c.name == campaign_name), None)
        
        # Check if character already exists for this campaign
        characters = search_characters_tool(query=name, campaign_id=campaign.id)
        character = next((c for c in characters if c.name == name and c.campaign_id == campaign.id), None)
        if character is None:
            created_character = create_character_tool(
                name=name,
                campaign_id=campaign.id,
                race=race,
                character_class=character_class
            )
            context.character_ids.append(created_character.id)
        else:
            context.character_ids.append(character.id)

@when('I create a character with the following extended details')
def step_impl_create_character_extended(context):
    table = context.table
    
    # Extract basic character properties
    name = None
    race = None
    character_class = None
    subclass = None
    background = None
    level = 1
    backstory = None
    
    # Extract nested properties
    ability_scores_data = {}
    modifiers_data = {}
    personality_data = {}
    
    # Process all the fields from the table
    for row in table:
        property_name = row['Property']
        value = row['Value']
        
        # Handle basic properties
        if property_name == 'name':
            name = value
        elif property_name == 'race':
            race = value
        elif property_name == 'class':
            character_class = value
        elif property_name == 'subclass':
            subclass = value
        elif property_name == 'background':
            background = value
        elif property_name == 'level':
            level = int(value)
        elif property_name == 'backstory':
            backstory = value
        # Handle ability scores
        elif property_name.startswith('ability_scores.'):
            ability = property_name.split('.')[1]
            ability_scores_data[ability] = int(value)
        # Handle modifiers
        elif property_name.startswith('modifiers.'):
            modifier = property_name.split('.')[1]
            modifiers_data[modifier] = int(value)
        # Handle personality traits
        elif property_name.startswith('personality.'):
            trait = property_name.split('.')[1]
            personality_data[trait] = value
    
    # Get the campaign
    campaigns = search_campaigns_tool(query="Lost Mines")
    campaign = next((c for c in campaigns if c.name == "Lost Mines"), None)
    
    # Check if character already exists for this campaign
    characters = search_characters_tool(query=name, campaign_id=campaign.id)
    character = next((c for c in characters if c.name == name and c.campaign_id == campaign.id), None)
    if character is None:
        # Create a Character instance with all the details
        created_character = create_character_tool(
            name=name,
            campaign_id=campaign.id,
            race=race,
            character_class=character_class,
            subclass=subclass,
            background=background,
            level=level,
            backstory=backstory,
            ability_scores=ability_scores_data if ability_scores_data else None,
            modifiers=modifiers_data if modifiers_data else None,
            personality=personality_data if personality_data else None
        )
        # Store the character ID for later steps
        context.character_id = created_character.id
        context.created_character = created_character
    else:
        context.character_id = character.id
        context.created_character = character

@when('I add the following proficiencies')
def step_impl_add_proficiencies(context):
    proficiencies = {}
    
    for row in context.table:
        type = row['Type']
        value = row['Value']
        proficiencies[type] = [item.strip() for item in value.split(',')]
    
    # Update the character with proficiencies
    update_character_tool(
        character_id=context.character_id, 
        proficiencies=proficiencies
    )

@when('I add the following equipment')
def step_impl_add_equipment(context):
    equipment = []
    
    # Each row is a single equipment item
    for row in context.table:
        equipment.append(row['Description'])
    
    # Update the character with equipment
    update_character_tool(
        character_id=context.character_id, 
        equipment=equipment
    )

@when('I add the following spells')
def step_impl_add_spells(context):
    spells = {}
    
    for row in context.table:
        type = row['Type']
        type_spells = row['Spells']
        spells[type] = [item.strip() for item in type_spells.split(',')]
    
    # Update the character with spells
    update_character_tool(
        character_id=context.character_id, 
        spells=spells
    )

@when('I add a familiar')
def step_impl_add_familiar(context):
    familiar = {}
    
    for row in context.table:
        property = row['Property']
        value = row['Value']
        if property == 'special_abilities':
            # Split comma-separated values into lists
            familiar[property] = [item.strip() for item in value.split(',')]
        else:
            familiar[property] = value
        
    
    # Update the character with familiar
    update_character_tool(
        character_id=context.character_id, 
        familiar=familiar
    )

@when('I add the following motivations')
def step_impl_add_motivations(context):
    motivations = []
    
    # Each row is a single motivation
    for row in context.table:
        motivations.append(row['Description'])
    
    # Update the character with motivations
    update_character_tool(
        character_id=context.character_id, 
        motivations=motivations
    )

@then('the character data should match the following JSON')
def step_impl_character_data_matches_json(context):
    # Get the character from the database
    character = get_character_resource(character_id=context.character_id)
    
    # Parse the expected JSON from the context.text
    expected_data = json.loads(context.text)
    
    # Create a dictionary from the character model for comparison
    actual_data = {
        "name": character.name,
        "race": character.race,
        "character_class": character.character_class,
        "subclass": character.subclass,
        "background": character.background,
        "level": character.level
    }
    
    # Add nested objects if they exist - using model_dump() instead of dict()
    if character.ability_scores:
        actual_data["ability_scores"] = character.ability_scores.model_dump()
    
    if character.modifiers:
        actual_data["modifiers"] = character.modifiers.model_dump()
    
    if character.proficiencies:
        actual_data["proficiencies"] = character.proficiencies.model_dump()
    
    if character.personality:
        actual_data["personality"] = character.personality.model_dump()
    
    if character.backstory:
        actual_data["backstory"] = character.backstory
    
    if character.equipment:
        actual_data["equipment"] = character.equipment
    
    if character.spells:
        actual_data["spells"] = character.spells.model_dump()
    
    if character.familiar:
        actual_data["familiar"] = character.familiar.model_dump()
    
    if character.motivations:
        actual_data["motivations"] = character.motivations
    
    # Compare the dictionaries
    for key, expected_value in expected_data.items():
        assert key in actual_data, f"Key '{key}' not found in character data"
        
        # For nested dictionaries, compare each field
        if isinstance(expected_value, dict):
            for nested_key, nested_value in expected_value.items():
                assert nested_key in actual_data[key], f"Nested key '{nested_key}' not found in '{key}'"
                assert actual_data[key][nested_key] == nested_value, \
                    f"Value mismatch for '{key}.{nested_key}': expected {nested_value}, got {actual_data[key][nested_key]}"
        # For lists, compare contents (order might not matter)
        elif isinstance(expected_value, list):
            assert sorted(actual_data[key]) == sorted(expected_value), \
                f"List mismatch for '{key}': expected {expected_value}, got {actual_data[key]}"
        # For simple values, direct comparison
        else:
            assert actual_data[key] == expected_value, \
                f"Value mismatch for '{key}': expected {expected_value}, got {actual_data[key]}"
    
    # Success if we get here
    assert True 