Feature: Campaign Management
  As a Dungeon Master
  I want to manage D&D campaigns
  So that I can organize my game information

  Scenario: Create a new campaign
    Given the D&D GM Assistant is running
    When I create a campaign with the following details:
      | name        | description                                |
      | Lost Mines  | A campaign set in the Forgotten Realms     |
    Then the campaign "Lost Mines" should be created successfully
    And the campaign "Lost Mines" should have description "A campaign set in the Forgotten Realms"

  Scenario: Update an existing campaign
    Given the D&D GM Assistant is running
    And a campaign "Lost Mines of Phandelver" exists
    When I update the campaign with the following details:
      | name                      | description                                        |
      | Lost Mines of Phandelver  | An adventure in Phandalin and the Sword Mountains  |
    Then the campaign "Lost Mines of Phandelver" should be updated successfully
    And the campaign "Lost Mines of Phandelver" should have description "An adventure in Phandalin and the Sword Mountains"

  Scenario: Delete a campaign
    Given the D&D GM Assistant is running
    And a campaign "Lost Mines Mistake" exists
    When I delete the campaign "Lost Mines Mistake"
    Then the campaign "Lost Mines Mistake" should be deleted successfully
    And the campaign "Lost Mines Mistake" should no longer be in the list of campaigns

  Scenario: Search for campaigns
    Given the D&D GM Assistant is running
    And the following campaigns exist:
      | name                    | description                            |
      | Lost Mines              | An adventure in Phandalin              |
      | Curse of Strahd         | A gothic horror campaign in Barovia    |
      | Storm King's Thunder    | A campaign about giants                |
    When I search for campaigns containing "horror"
    Then the search results should include "Curse of Strahd"
    And the search results should not include "Lost Mines"
    And the search results should not include "Storm King's Thunder"

  # Scenario: Search with blank string
  #   Given the D&D GM Assistant is running
  #   And an empty database
  #   And the following campaigns exist:
  #     | name                    | description                            |
  #     | Lost Mines              | An adventure in Phandalin              |
  #     | Curse of Strahd         | A gothic horror campaign in Barovia    |
  #     | Storm King's Thunder    | A campaign about giants                |
  #   When I search for campaigns containing "''"
  #   Then the search results should include "Lost Mines"
  #   And the search results should include "Curse of Strahd"
  #   And the search results should include "Storm King's Thunder" 