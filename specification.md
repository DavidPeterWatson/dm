# D&D Game Master Assistant MCP Server Specification

## Overview

This document specifies a Model Context Protocol (MCP) server designed to assist Claude in running Dungeons & Dragons games as a Dungeon Master. The server will provide tools for managing campaign information, storing game data, and retrieving relevant information during gameplay sessions.

## Purpose

The D&D Game Master Assistant MCP server will enhance Claude's capabilities as a Dungeon Master by:

1. Storing and organizing campaign information in a structured format
2. Providing quick access to game elements (NPCs, locations, items, etc.)
3. Maintaining game state and history across sessions
4. Offering tools to manage game mechanics and rules
5. Managing player characters and their progression

## Technology Stack

- **Language**: Python 3.10+
- **MCP Implementation**: fastmcp as per the documentation at https://github.com/modelcontextprotocol/fastmcp/tree/main
- **Database**: MongoDB (for document-based storage of campaign data)
- **Testing**: Behave (for BDD-style testing)
- **Additional Libraries**:
  - `pydantic` (for data validation)
  - `pymongo` (for MongoDB operations)
  - `motor` (for asynchronous MongoDB operations)
  - `rich` (for formatted console output during development)

## Project Structure

```
dnd-gm-assistant/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── dm.py                 # Main MCP server implementation
│   ├── database/
│   │   ├── __init__.py
│   │   ├── schema.py             # Database schema definitions
│   │   └── db_operations.py         # default Database operations
│   │   └── campaign_operations.py         # Database CRUD operations
│   │   └── character_operations.py         # Database CRUD operations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── campaign.py           # Data models for campaign elements
│   │   └── character.py          # Data models for character elements
│   └── utils/
│       ├── __init__.py
│       └── helpers.py            # Utility functions
├── tests/
│   ├── __init__.py
│   ├── features/
│   │   ├── campaign_management.feature
│   │   └── character_management.feature
│   └── steps/
│       ├── __init__.py
│       ├── campaign_steps.py
│       └── character_steps.py

└── data/
    └── mongodb/
```

## Database Schema

The SQLite database will store campaign information in JSON format with appropriate indexing for efficient searching:

### Tables

1. **campaigns**
   - `id`: INTEGER PRIMARY KEY
   - `name`: TEXT NOT NULL
   - `description`: TEXT
   - `data`: JSON
   - `created_at`: TIMESTAMP
   - `updated_at`: TIMESTAMP

2. **characters**
   - `id`: INTEGER PRIMARY KEY
   - `campaign_id`: INTEGER REFERENCES campaigns(id)
   - `name`: TEXT NOT NULL
   - `player_name`: TEXT
   - `data`: JSON
   - `created_at`: TIMESTAMP
   - `updated_at`: TIMESTAMP

## MCP Server Features

### Resources

1. **Campaign Information**
   - `campaign://{campaign_id}` - Get campaign details
   - `campaign://{campaign_id}/summary` - Get campaign summary
   - `campaign://list` - List all campaigns

2. **Character Information**
   - `character://{character_id}` - Get character details
   - `character://{character_id}/summary` - Get character summary
   - `character://list` - List all characters
   - `character://campaign/{campaign_id}/list` - List all characters in a campaign


### Tools

1. **Campaign Management**
   - `create_campaign` - Create a new campaign
   - `update_campaign` - Update campaign details
   - `delete_campaign` - Delete a campaign
   - `search_campaigns` - Search campaigns by name or description

2. **Character Management**
   - `create_character` - Create a new character
   - `update_character` - Update character details
   - `delete_character` - Delete a character
   - `search_characters` - Search characters by name, race, class, etc.
   - `level_up_character` - Handle character level progression
   - `track_character_progress` - Update character campaign progress


### Prompts

1. **Campaign Creation**
   - `create_new_campaign` - Guide for creating a new campaign

2. **Character Creation**
   - `create_new_character` - Guide for creating a new character


## BDD Feature Files

### Campaign Management Feature

```gherkin
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
    And the campaign should have the provided description

  Scenario: Update an existing campaign
    Given the D&D GM Assistant is running
    And a campaign "Lost Mines" exists
    When I update the campaign with the following details:
      | name        | description                                        |
      | Lost Mines  | An adventure in Phandalin and the Sword Mountains  |
    Then the campaign "Lost Mines" should be updated successfully
    And the campaign should have the new description

  Scenario: Delete a campaign
    Given the D&D GM Assistant is running
    And a campaign "Lost Mines" exists
    When I delete the campaign "Lost Mines"
    Then the campaign "Lost Mines" should be deleted successfully
    And the campaign should no longer be in the list of campaigns

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
```

### Character Management Feature

```gherkin
Feature: Character Management
  As a Dungeon Master
  I want to manage D&D characters
  So that I can track player information and progress

  Scenario: Create a new character
    Given the D&D GM Assistant is running
    And a campaign "Lost Mines" exists
    When I create a character with the following details:
      | name           | race          | class   | campaign_id |
      | Fizwick        | Forest Gnome  | Wizard  | 1           |
    Then the character "Fizwick" should be created successfully
    And the character should be associated with the "Lost Mines" campaign

  Scenario: Update an existing character
    Given the D&D GM Assistant is running
    And a character "Fizwick" exists
    When I update the character with the following details:
      | level | ability_scores.intelligence |
      | 2     | 19                          |
    Then the character "Fizwick" should be updated successfully
    And the character's level should be 2
    And the character's intelligence score should be 19

  Scenario: Delete a character
    Given the D&D GM Assistant is running
    And a character "Fizwick" exists
    When I delete the character "Fizwick"
    Then the character "Fizwick" should be deleted successfully
    And the character should no longer be in the list of characters

  Scenario: Search for characters
    Given the D&D GM Assistant is running
    And the following characters exist:
      | name           | race          | class     | campaign_id |
      | Fizwick        | Forest Gnome  | Wizard    | 1           |
      | Bruenor        | Dwarf         | Fighter   | 1           |
      | Drizzt         | Drow          | Ranger    | 2           |
    When I search for characters with class "Wizard"
    Then the search results should include "Fizwick"
    And the search results should not include "Bruenor"
    And the search results should not include "Drizzt"

  Scenario: Track character campaign progress
    Given the D&D GM Assistant is running
    And a character "Fizwick" exists
    When I update the character's campaign progress with:
      | current_location                                      | key_discoveries                                    |
      | Entrance to Mythalar's sanctuary in Whispering Ruins  | Inkwhisper is an 'Awakened Conduit'               |
    Then the character's campaign progress should be updated successfully
    And the character's current location should be "Entrance to Mythalar's sanctuary in Whispering Ruins"
```

## Implementation Considerations

1. **Database Initialization**
   - The server should automatically create the SQLite database and tables if they don't exist
   - Include a migration system for future schema updates

2. **Error Handling**
   - Implement comprehensive error handling for database operations
   - Provide clear error messages for MCP clients

3. **Performance**
   - Use appropriate indexing for frequently queried fields
   - Implement caching for frequently accessed data

4. **Security**
   - Validate all input data before storing in the database
   - Sanitize all output to prevent injection attacks

5. **Extensibility**
   - Design the system to be easily extended with new features
   - Use interfaces and abstract classes where appropriate

## Future Enhancements

1. **Combat Tracker**
   - Initiative tracking
   - HP and status effect management

2. **Random Generators**
   - NPC generator
   - Town generator
   - Dungeon generator

3. **Rules Reference**
   - Quick access to common rules
   - Spell database

4. **Media Support**
   - Store and retrieve images for maps, characters, etc.
   - Audio clips for ambiance

5. **Character Sheet Integration**
   - PDF export of character sheets
   - Integration with popular VTT platforms
   - Automated level-up calculations

6. **Character Progression Tracking**
   - XP and milestone tracking
   - Inventory management
   - Spell slot usage and rest tracking
   
## Conclusion

This specification outlines a comprehensive MCP server for assisting Claude in running D&D games as a Dungeon Master. The server will provide tools for managing campaign information, characters, locations, items, and game sessions, all stored in a SQLite database for easy portability and maintenance.

The BDD-style feature files provide a clear set of requirements and acceptance criteria for the implementation, ensuring that the server meets the needs of D&D Dungeon Masters. 