from behave import given, when, then
from src.database.campaign_operations import (
    create_campaign, get_campaign, list_campaigns, 
    delete_campaign, update_campaign, search_campaigns,
    delete_all_campaigns, get_campaign_by_name
)

from src.models.campaign import Campaign



@given('only the following campaigns exist')
def step_impl_only_these_campaigns_exist(context):
    # First clear the database
    delete_all_campaigns()
    # Then create the specified campaigns
    context.campaign_ids = []
    for row in context.table:
        name = row['name']
        description = row['description']
        campaign = create_campaign(name, description)
        context.campaign_ids.append(campaign.id)

@given('a campaign "{name}" exists')
def step_impl_campaign_exists(context, name):
    campaign = create_campaign(name, f"Description for {name}")
    context.campaign_id = campaign.id

@when('I create a campaign with the following details')
def step_impl_create_campaign_details(context):
    table = context.table
    for row in table:
        name = row['name']
        description = row['description']
        campaign = create_campaign(name, description)
        context.created_campaign = campaign
        context.campaign_id = campaign.id

@when('I update the campaign with the following details')
def step_impl_update_campaign_details(context):
    table = context.table
    for row in table:
        name = row['name']
        description = row['description']
        updated_campaign = update_campaign(context.campaign_id, name, description)
        context.updated_campaign = updated_campaign

@when('I delete the campaign "{name}"')
def step_impl_delete_campaign(context, name):
    campaign = get_campaign_by_name(name)
    result = delete_campaign(campaign.id)
    context.delete_result = result
    context.deleted_campaign_name = name

@when('I search for campaigns containing "{query}"')
def step_impl_search_campaigns(context, query):
    context.search_results = search_campaigns(query)

@then('the campaign "{name}" should be created successfully')
def step_impl_campaign_created(context, name):
    campaign = get_campaign_by_name(name)
    campaign = get_campaign(campaign.id)
    assert campaign.name == name

@then('the campaign "{name}" should be updated successfully')
def step_impl_campaign_updated(context, name):
    campaign = get_campaign(context.updated_campaign.id)
    assert campaign.name == name

@then('the campaign "{name}" should be deleted successfully')
def step_impl_campaign_deleted(context, name):
    # First verify that the delete operation returned True
    assert context.delete_result is True, "Delete operation did not return True"
    
    # Then try to get the campaign and expect a ValueError
    try:
        get_campaign_by_name(name)
        assert False, "Campaign was not deleted - still retrievable by name"
    except ValueError:
        # This is the expected path - campaign should not be found
        pass

@then('the campaign search results should include "{name}"')
def step_impl_search_include(context, name):
    campaign_names = [campaign.name for campaign in context.search_results]
    assert name in campaign_names

@then('the campaign search results should not include "{name}"')
def step_impl_search_exclude(context, name):
    campaign_names = [campaign.name for campaign in context.search_results]
    assert name not in campaign_names

@given('the following campaigns exist')
def step_impl_multiple_campaigns_exist(context):
    context.campaign_ids = []
    for row in context.table:
        name = row['name']
        description = row['description']
        campaign = create_campaign(name, description)
        context.campaign_ids.append(campaign.id)

@then('the campaign "{name}" should have description "{description}"')
def step_impl_check_specific_description(context, name, description):
    campaign = get_campaign(context.campaign_id)
    assert campaign.description == description

@then('the campaign "{name}" should no longer be in the list of campaigns')
def step_impl_specific_campaign_not_in_list(context, name):
    campaigns = list_campaigns()
    campaign_names = [campaign.name for campaign in campaigns]
    assert name not in campaign_names 