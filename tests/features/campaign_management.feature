Feature: Campaign Management
  As a Dungeon Master
  I want to manage D&D campaigns
  So that I can organize my game information

  Scenario: Create a new campaign
    Given there are no campaigns
    When I create a campaign with the following details:
      | name        | description                                |
      | Lost Mines  | A campaign set in the Forgotten Realms     |
    Then the campaign "Lost Mines" should be created successfully
    And the campaign "Lost Mines" should have description "A campaign set in the Forgotten Realms"

  Scenario: Update an existing campaign
    Given there are no campaigns
    And a campaign "Lost Mines of Phandelver" exists
    When I update campaigns with the following details:
      | name                      | description                                        |
      | Lost Mines of Phandelver  | An adventure in Phandalin and the Sword Mountains  |
    Then the campaign "Lost Mines of Phandelver" should be updated successfully
    And the campaign "Lost Mines of Phandelver" should have description "An adventure in Phandalin and the Sword Mountains"

  Scenario: Empty the database
    Given there are no campaigns
    Then the campaign "Lost Mines" should no longer be in the list of campaigns

  Scenario: Delete a campaign
    Given there are no campaigns
    And a campaign "Delete Lost Mines" exists
    When I delete the campaign "Delete Lost Mines"
    Then the campaign "Delete Lost Mines" should be deleted successfully
    And the campaign "Delete Lost Mines" should no longer be in the list of campaigns

  Scenario: Search for campaigns
    Given there are no campaigns
    And the following campaigns exist:
      | name                    | description                            |
      | Lost Mines              | An adventure in Phandalin              |
      | Curse of Strahd         | A gothic horror campaign in Barovia    |
      | Storm King's Thunder    | A campaign about giants                |
    When I search for campaigns containing "horror"
    Then the campaign search results should include "Curse of Strahd"
    And the campaign search results should not include "Lost Mines"
    And the campaign search results should not include "Storm King's Thunder"

  Scenario: Cannot create campaigns with duplicate names
    Given there are no campaigns
    When I create a campaign named "Unique Campaign" with description "This is a unique campaign"
    Then the campaign "Unique Campaign" should be created successfully
    When I create a campaign named "Unique Campaign" with description "This is a duplicate name"
    Then I should see an error that the campaign name already exists 