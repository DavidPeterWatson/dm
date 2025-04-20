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

  Scenario: Search for characters by class
    Given the D&D GM Assistant is running
    And an empty database
    And a campaign "Lost Mines" exists
    And the following characters exist:
      | name           | race          | class     | campaign_name |
      | Fizwick        | Forest Gnome  | Wizard    | Lost Mines           |
      | Bruenor        | Dwarf         | Fighter   | Lost Mines           |
      | Drizzt         | Drow          | Ranger    | Lost Mines           |
    When I search for characters with class "Wizard"
    Then the character class search results should include "Fizwick"
    And the character class search results should not include "Bruenor"
    And the character class search results should not include "Drizzt"

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

  Scenario: Create a character with all extended fields
    Given the D&D GM Assistant is running
    And an empty database
    And a campaign "Lost Mines" exists
    When I create a character with the following extended details:
      | Property                          | Value                                |
      | name                          | Fizwick Quillsharp                                |
      | race                          | Forest Gnome                                      |
      | class                         | Wizard                                            |
      | subclass                      | Order of Scribes                                  |
      | background                    | Sage                                              |
      | level                         | 1                                                 |
      | ability_scores.strength       | 10                                                |
      | ability_scores.dexterity      | 15                                                |
      | ability_scores.constitution   | 15                                                |
      | ability_scores.intelligence   | 18                                                |
      | ability_scores.wisdom         | 12                                                |
      | ability_scores.charisma       | 11                                                |
      | modifiers.strength            | 0                                                 |
      | modifiers.dexterity           | 2                                                 |
      | modifiers.constitution        | 2                                                 |
      | modifiers.intelligence        | 4                                                 |
      | modifiers.wisdom              | 1                                                 |
      | modifiers.charisma            | 0                                                 |
      | personality.trait             | Uses polysyllabic words that convey the impression of great erudition |
      | personality.ideal             | Knowledge is the path to power and self-improvement |
      | personality.bond              | My magical quill, Inkwhisper, is my most precious possession |
      | personality.flaw              | I become obsessed with uncovering knowledge       |
      | backstory                     | Fizwick grew up in a small gnomish enclave deep within the Neverwinter Wood |
    And I add the following proficiencies:
      | Type                          | Value                                |
      | saving_throws  | Intelligence,Wisdom                                |
      | skills        | Arcana,History,Investigation,Insight               |
      | weapons       | Daggers,Darts,Slings,Quarterstaffs,Light Crossbows |
      | languages     | Common,Gnomish,Elvish,Sylvan                       |
    And I add the following equipment:
      | Description                          |
      | Quarterstaff with an orb embedded at the top                |
      | Spellbook                                                   |
      | Scholar's pack                                              |
      | Inkwhisper (sentient magical quill)                         |
    And I add the following spells:
      | Type | Spells |
      | cantrips | Prestidigitation,Fire Bolt,Mage Hand,Dancing Lights,Minor Illusion |
      | level_1  | Find Familiar,Mage Armor,Identify,Chromatic Orb,Detect Magic      |
    And I add a familiar:
      | Property                          | Value                                |
      | type             | Owl                                      |
      | name             | Penumbra                                 |
      | special_abilities | Flyby,Darkvision,Keen Hearing and Sight |
    And I add the following motivations:
      | Description                          |
      | Uncover the secrets of his magical quill Inkwhisper                |
      | Learn more about the ancient elven civilization                    |
      | Discover the greater repository of knowledge in Neverwinter Wood   |
    Then the character "Fizwick Quillsharp" should be created successfully
    And the character data should match the following JSON:
      """
      {
        "name": "Fizwick Quillsharp",
        "race": "Forest Gnome",
        "character_class": "Wizard",
        "subclass": "Order of Scribes",
        "background": "Sage",
        "level": 1,
        "ability_scores": {
          "strength": 10,
          "dexterity": 15,
          "constitution": 15,
          "intelligence": 18,
          "wisdom": 12,
          "charisma": 11
        },
        "modifiers": {
          "strength": 0,
          "dexterity": 2,
          "constitution": 2,
          "intelligence": 4,
          "wisdom": 1,
          "charisma": 0
        },
        "proficiencies": {
          "saving_throws": ["Intelligence", "Wisdom"],
          "skills": ["Arcana", "History", "Investigation", "Insight"],
          "weapons": ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light Crossbows"],
          "languages": ["Common", "Gnomish", "Elvish", "Sylvan"]
        },
        "personality": {
          "trait": "Uses polysyllabic words that convey the impression of great erudition",
          "ideal": "Knowledge is the path to power and self-improvement",
          "bond": "My magical quill, Inkwhisper, is my most precious possession",
          "flaw": "I become obsessed with uncovering knowledge"
        },
        "backstory": "Fizwick grew up in a small gnomish enclave deep within the Neverwinter Wood",
        "equipment": [
          "Quarterstaff with an orb embedded at the top",
          "Spellbook",
          "Scholar's pack",
          "Inkwhisper (sentient magical quill)"
        ],
        "spells": {
          "cantrips": ["Prestidigitation", "Fire Bolt", "Mage Hand", "Dancing Lights", "Minor Illusion"],
          "level_1": ["Find Familiar", "Mage Armor", "Identify", "Chromatic Orb", "Detect Magic"]
        },
        "familiar": {
          "type": "Owl",
          "name": "Penumbra",
          "special_abilities": ["Flyby", "Darkvision", "Keen Hearing and Sight"]
        },
        "motivations": [
          "Uncover the secrets of his magical quill Inkwhisper",
          "Learn more about the ancient elven civilization",
          "Discover the greater repository of knowledge in Neverwinter Wood"
        ]
      }
      """ 