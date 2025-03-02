Feature: Character Management
  As a Dungeon Master
  I want to manage D&D characters
  So that I can track player information and progress

  Scenario: Create a new character
    Given the D&D GM Assistant is running
    And an empty database
    And a campaign "Lost Mines" exists
    When I create a character with the following details:
      | name           | race          | class   | campaign_name |
      | Fizwick        | Forest Gnome  | Wizard  | Lost Mines           |
    Then the character "Fizwick" should be created successfully
    And Fizwick should be associated with the "Lost Mines" campaign

  Scenario: Update an existing character
    Given the D&D GM Assistant is running
    And an empty database
    And a campaign "Lost Mines" exists
    And a character "Fizwick" exists for "Lost Mines" campaign
    When I update the character with the following details:
      | level | ability_scores.intelligence |
      | 2     | 19                          |
    Then the character "Fizwick" should be updated successfully
    And the character's level should be 2
    And the character's intelligence score should be 19

  Scenario: Delete a character
    Given the D&D GM Assistant is running
    And an empty database
    And a campaign "Lost Mines" exists
    And a character "Fizwick" exists for "Lost Mines" campaign
    When I delete the character "Fizwick"
    Then the character "Fizwick" should be deleted successfully
    And the character should no longer be in the list of characters

  Scenario: Search for characters
    Given the D&D GM Assistant is running
    And a campaign "Lost Mines" exists
    And the following characters exist:
      | name           | race          | class     | campaign_name |
      | Fizwick        | Forest Gnome  | Wizard    | Lost Mines           |
      | Bruenor        | Dwarf         | Fighter   | Lost Mines           |
      | Drizzt         | Drow          | Ranger    | Lost Mines           |
    When I search for characters with class "Wizard"
    Then the character search results should include "Fizwick"
    And the character search results should not include "Bruenor"
    And the character search results should not include "Drizzt"

  Scenario: Track character campaign progress
    Given the D&D GM Assistant is running
    And an empty database
    And a campaign "Lost Mines" exists
    And a character "Fizwick" exists for "Lost Mines" campaign
    When I update the character's campaign progress with:
      | current_location                                      | key_discoveries                                    |
      | Entrance to Mythalar's sanctuary in Whispering Ruins  | Inkwhisper is an 'Awakened Conduit'               |
    Then the character's campaign progress should be updated successfully
    And the character's current location should be "Entrance to Mythalar's sanctuary in Whispering Ruins" 