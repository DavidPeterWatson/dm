from behave import given, when, then
from src.dm import (
    create_campaign_tool,
    update_campaign_tool,
    delete_campaign_tool,
    search_campaigns_tool,
    get_campaign_resource,
    list_campaigns_resource,
    delete_all_campaigns_tool
)

import logging
logger = logging.getLogger('behave')

@given('there are no campaigns')
def step_impl_no_campaigns(context):
    # Clear the database
    delete_all_campaigns_tool()

@given('a campaign "{name}" exists')
def step_impl_campaign_exists(context, name):
    campaign = create_campaign_tool(name=name, description=f"Description for {name}")

@when('I create a campaign with the following details')
def step_impl_create_campaign_details(context):
    table = context.table
    for row in table:
        name = row['name']
        description = row['description']
        campaign = create_campaign_tool(name=name, description=description)
        context.created_campaign = campaign

@when('I create a campaign named "{name}" with description "{description}"')
def step_create_campaign(context, name, description):
    try:
        campaign = create_campaign_tool(name=name, description=description)
        context.campaign_id = campaign.id
        context.campaign_name_already_exists_error = None
    except ValueError as e:
        context.campaign_name_already_exists_error = str(e)
        context.campaign_id = None

@when('I update campaigns with the following details')
def step_impl_update_campaign_details(context):
    table = context.table
    for row in table:
        # We need to find campaign by name first
        campaigns = search_campaigns_tool(query=row['name'])
        campaign = next((c for c in campaigns if c.name == row['name']), None)
        name = row['name']
        description = row['description']
        context.updated_campaign = update_campaign_tool(campaign_id=campaign.id, name=name, description=description)

@when('I delete the campaign "{name}"')
def step_impl_delete_campaign(context, name):
    # Find campaign by name first
    campaigns = search_campaigns_tool(query=name)
    campaign = next((c for c in campaigns if c.name == name), None)
    result = delete_campaign_tool(campaign_id=campaign.id)
    context.delete_result = result
    context.deleted_campaign_name = name

@when('I search for campaigns containing "{query}"')
def step_impl_search_campaigns(context, query):
    context.search_results = search_campaigns_tool(query=query)

@then('the campaign "{name}" should be created successfully')
def step_impl_campaign_created(context, name):
    # Search for campaign by name
    campaigns = search_campaigns_tool(query=name)
    campaign = next((c for c in campaigns if c.name == name), None)
    assert campaign is not None
    campaign = get_campaign_resource(campaign_id=campaign.id)
    assert campaign.name == name

@then('the campaign "{name}" should be updated successfully')
def step_impl_campaign_updated(context, name):
    # Search for campaign by name
    campaigns = search_campaigns_tool(query=name)
    campaign = next((c for c in campaigns if c.name == name), None)
    updated_campaign = get_campaign_resource(campaign_id=context.updated_campaign.id)
    assert campaign.id == updated_campaign.id
    assert campaign.name == updated_campaign.name
    assert campaign.description == updated_campaign.description

@then('the campaign "{name}" should be deleted successfully')
def step_impl_campaign_deleted(context, name):
    # Search for campaign by name
    campaigns = search_campaigns_tool(query=name)
    campaign = next((c for c in campaigns if c.name == name), None)
    assert campaign is None

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
        campaign = create_campaign_tool(name=name, description=description)
        context.campaign_ids.append(campaign.id)

@then('the campaign "{name}" should have description "{description}"')
def step_impl_check_specific_description(context, name, description):
    # Search for campaign by name
    campaigns = search_campaigns_tool(query=name)
    campaign = next((c for c in campaigns if c.name == name), None)
    assert campaign.description == description

@then('the campaign "{name}" should no longer be in the list of campaigns')
def step_impl_specific_campaign_not_in_list(context, name):
    logger.info(f"DEBUG: Checking if campaign '{name}' is no longer in the list of campaigns")
    campaigns = list_campaigns_resource()
    logger.info(f"DEBUG: Result of list_campaigns: {[c.name for c in campaigns]}")
    campaign_names = [campaign.name for campaign in campaigns]
    assert name not in campaign_names
    logger.info(f"DEBUG: Successfully verified campaign '{name}' is not in the list")

@then('I should see an error that the campaign name already exists')
def step_campaign_name_exists_error(context):
    assert context.campaign_name_already_exists_error is not None
    assert "already exists" in context.campaign_name_already_exists_error 