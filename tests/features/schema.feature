Feature: Schema

  Scenario: Viewing labels after adding new label
    Given I start cycli
    And The prompt is visible
    And I add a node with a label
    When I refresh the schema
    And I ask to see the labels
    Then I should see the new label