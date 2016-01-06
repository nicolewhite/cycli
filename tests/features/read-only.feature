Feature: Read-only mode

  Scenario: Executing write query in read-only mode
    Given I start cycli in read-only mode
    And The prompt is visible
    When I execute a write query
    Then I should be told I'm in read-only mode