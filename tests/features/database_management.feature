Feature: Database Management
    As a Dungeon Master
    I want to manage the application database
    So that I can view and control database state and information

    Scenario: Get database info
        Given the database is initialized
        When I request the database info
        Then I should see the database name
        And I should see the number of campaigns
        And I should see the number of characters
        And I should see the number of settings 