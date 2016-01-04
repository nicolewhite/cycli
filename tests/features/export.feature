Feature: Exporting Parameters

  Scenario: Setting a string parameter
    Given I start cycli
    And The prompt is visible
    And I set an env var equal to a string
    When I ask for my env vars
    Then I should see the string env var

  Scenario: Setting a numeric parameter
    Given I start cycli
    And The prompt is visible
    And I set an env var equal to a number
    When I ask for my env vars
    Then I should see the numeric env var

  Scenario: Setting a boolean parameter
    Given I start cycli
    And The prompt is visible
    And I set an env var equal to a boolean
    When I ask for my env vars
    Then I should see the boolean env var

  Scenario: Setting a list comprehension parameter
    Given I start cycli
    And The prompt is visible
    And I set an env var equal to a Python list comprehension
    When I ask for my env vars
    Then I should see the list env var

  Scenario: Accessing a parameter by key
    Given I start cycli
    And The prompt is visible
    And I set an env var equal to a string
    When I ask for the string env var by key
    Then I should see the string env var without the key