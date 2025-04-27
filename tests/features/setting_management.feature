Feature: Setting Management
    As a Dungeon Master
    I want to manage campaign settings
    So that I can create and organize detailed locations for my game

    Scenario: Create a new setting with only required fields
        Given there are no settings
        When I create a setting with the following details:
            | field        | value       |
            | setting_type | City        |
            | name         | Waterdeep   |
            | region       | Sword Coast |
            | scale        | Large       |
            | population   | 100,000     |
        Then the setting "Waterdeep" should be created successfully
        And the setting should have the following details:
            | field        | value       |
            | setting_type | City        |
            | name         | Waterdeep   |
            | region       | Sword Coast |
            | scale        | Large       |
            | population   | 100,000     |

    Scenario: Create a setting with complete details
        Given there are no settings
        When I create a setting with the following details:
            | field                | value                                    |
            | setting_type         | City                                     |
            | name                 | Waterdeep                                |
            | region               | Sword Coast                              |
            | scale                | Large metropolis                         |
            | population           | ~100,000 diverse inhabitants             |
            | first_impression     | A bustling coastal metropolis            |
            | distinctive_features | Castle Waterdeep, Harbor Ward            |
            | atmosphere           | Busy streets filled with traders         |
            | key_locations        | Yawning Portal, Blackstaff Tower         |
            | points_of_interest   | Undermountain entrance, Dock Ward sewers |
            | travel_routes        | Trade Way, Long Road, Sea routes         |
            | factions             | Lords Alliance, Harpers, Zhentarim       |
            | power_structure      | Masked Lords and Open Lord               |
            | local_customs        | Masked governance, Guild laws            |
            | economic_basis       | Trade, Crafting, Maritime commerce       |
            | origin               | Founded by Aghairon                      |
            | recent_history       | Dragon attack, Guild conflicts           |
            | hidden_past          | Ancient dungeons beneath                 |
        Then the setting "Waterdeep" should be created successfully
        And the setting should have the following details:
            | field                | value                                    |
            | setting_type         | City                                     |
            | name                 | Waterdeep                                |
            | region               | Sword Coast                              |
            | scale                | Large metropolis                         |
            | population           | ~100,000 diverse inhabitants             |
            | first_impression     | A bustling coastal metropolis            |
            | distinctive_features | Castle Waterdeep, Harbor Ward            |
            | atmosphere           | Busy streets filled with traders         |
            | key_locations        | Yawning Portal, Blackstaff Tower         |
            | points_of_interest   | Undermountain entrance, Dock Ward sewers |
            | travel_routes        | Trade Way, Long Road, Sea routes         |
            | factions             | Lords Alliance, Harpers, Zhentarim       |
            | power_structure      | Masked Lords and Open Lord               |
            | local_customs        | Masked governance, Guild laws            |
            | economic_basis       | Trade, Crafting, Maritime commerce       |
            | origin               | Founded by Aghairon                      |
            | recent_history       | Dragon attack, Guild conflicts           |
            | hidden_past          | Ancient dungeons beneath                 |

    Scenario: Update multiple setting properties at once
        Given there are no settings
        And a setting "Waterdeep" exists
        When I update the setting with the following details:
            | field           | value                                            |
            | population      | ~130,000 diverse inhabitants                     |
            | power_structure | Masked Lords, Open Lord, and Guild Councils      |
            | factions        | Lords Alliance, Harpers, Zhentarim, Force Grey   |
            | hidden_past     | Ancient dungeons and forgotten catacombs beneath |
        Then the setting "Waterdeep" should be updated successfully
        And the setting should have the updated fields:
            | field           | value                                            |
            | population      | ~130,000 diverse inhabitants                     |
            | power_structure | Masked Lords, Open Lord, and Guild Councils      |
            | factions        | Lords Alliance, Harpers, Zhentarim, Force Grey   |
            | hidden_past     | Ancient dungeons and forgotten catacombs beneath |

    Scenario: Delete a setting
        Given there are no settings
        And a setting "Waterdeep" exists
        When I delete the setting "Waterdeep"
        Then the setting "Waterdeep" should be deleted successfully
        And the setting "Waterdeep" should no longer be in the list of settings

    Scenario: Cannot create settings with duplicate names
        Given there are no settings
        When I create a setting named "Unique Setting" of type "City"
        Then the setting "Unique Setting" should be created successfully
        When I create a setting named "Unique Setting" of type "Town"
        Then I should see an error that the setting name already exists

    Scenario: List settings when no settings exist
        Given there are no settings
        When I list all settings
        Then the settings list should be empty
        And I should receive a message indicating no settings exist

    Scenario: Create a World-level setting
        Given there are no settings
        When I create a setting with the following details:
            | field                | value                                               |
            | setting_type         | World                                               |
            | name                 | Ardena                                              |
            | region               | Global                                              |
            | scale                | Planet                                              |
            | population           | Various civilizations across two known continents   |
            | first_impression     | A world of untamed wilderness and ancient mysteries |
            | distinctive_features | Towering mountains, vast oceans, ancient forests    |
        Then the setting "Ardena" should be created successfully
        And the setting should have the following details:
            | field                | value                                               |
            | setting_type         | World                                               |
            | name                 | Ardena                                              |
            | region               | Global                                              |
            | scale                | Planet                                              |
            | population           | Various civilizations across two known continents   |
            | first_impression     | A world of untamed wilderness and ancient mysteries |
            | distinctive_features | Towering mountains, vast oceans, ancient forests    |

    Scenario: Create a Region-level setting
        Given there are no settings
        When I create a setting with the following details:
            | field                | value                                                   |
            | setting_type         | Region                                                  |
            | name                 | Shadowreach Highlands                                   |
            | region               | Northern Orrhaga                                        |
            | scale                | Large mountainous region                                |
            | population           | Scattered settlements and nomadic tribes                |
            | first_impression     | Towering mountains shrouded in mist and ancient secrets |
            | distinctive_features | Jagged peaks, hidden valleys, ancient ruins             |
        Then the setting "Shadowreach Highlands" should be created successfully
        And the setting should have the following details:
            | field                | value                                                   |
            | setting_type         | Region                                                  |
            | name                 | Shadowreach Highlands                                   |
            | region               | Northern Orrhaga                                        |
            | scale                | Large mountainous region                                |
            | population           | Scattered settlements and nomadic tribes                |
            | first_impression     | Towering mountains shrouded in mist and ancient secrets |
            | distinctive_features | Jagged peaks, hidden valleys, ancient ruins             |

    Scenario: Create related settings with parent-child relationships
        Given there are no settings
        When I create a setting with the following details:
            | field        | value   |
            | setting_type | World   |
            | name         | Ardena  |
            | region       | Global  |
            | scale        | Planet  |
            | population   | Various |
        Then the setting "Ardena" should be created successfully
        When I create a setting with the following details:
            | field        | value                  |
            | setting_type | Continent              |
            | name         | Orrhaga                |
            | region       | Northern Hemisphere    |
            | scale        | Supercontinent         |
            | population   | Multiple civilizations |
            | parent_id    | {Ardena's ID}          |
        Then the setting "Orrhaga" should be created successfully
        And the setting "Orrhaga" should have "Ardena" as its parent setting
        When I create a setting with the following details:
            | field        | value                    |
            | setting_type | Region                   |
            | name         | Shadowreach Highlands    |
            | region       | Northern Orrhaga         |
            | scale        | Large mountainous region |
            | population   | Scattered tribes         |
            | parent_id    | {Orrhaga's ID}           |
        Then the setting "Shadowreach Highlands" should be created successfully
        And the setting "Shadowreach Highlands" should have "Orrhaga" as its parent setting
        And the setting "Ardena" should have "Orrhaga" as a child setting
        And the setting "Orrhaga" should have "Shadowreach Highlands" as a child setting

    Scenario: Search for settings by text or type
        Given there are no settings
        And the following settings exist:
            | name               | setting_type | region           |
            | Waterdeep          | City         | Sword Coast      |
            | Phandalin          | Town         | Sword Coast      |
            | Barovia            | Region       | Domains of Dread |
            | Neverwinter Forest | Forest       | Sword Coast      |
        When I search for settings containing "Sword Coast"
        Then the setting search results should include "Waterdeep"
        And the setting search results should include "Phandalin"
        And the setting search results should not include "Barovia"
        When I search for settings of type "City"
        Then the setting search results should include "Waterdeep"
        And the setting search results should not include "Phandalin"
        And the setting search results should not include "Neverwinter Forest"

    Scenario: Error handling when updating settings (invalid JSON)
        Given there are no settings
        And a setting "Waterdeep" exists
        When I update the setting with the following JSON
            """
            {
            "population": "~100,000"
            "factions": Lords Alliance, Harpers, Zhentarim
            }
            """
        Then I should see an error about invalid JSON format

    Scenario: Error handling when updating settings (invalid field type)
        Given there are no settings
        And a setting "Waterdeep" exists
        When I update the setting with the following JSON
            """
            {
                "population": 100000,
                "scale": [
                    "Large",
                    "Metropolis"
                ]
            }
            """
        Then I should see an error about invalid field types

    Scenario: Error handling when updating settings (unknown fields)
        Given there are no settings
        And a setting "Waterdeep" exists
        When I update the setting with the following JSON
            """
            {
                "population": "~100,000 inhabitants",
                "nonexistent_field": "Some value"
            }
            """
        Then I should see a warning: "Warning: Unknown fields ignored: nonexistent_field"
        And the setting should be updated with valid fields only