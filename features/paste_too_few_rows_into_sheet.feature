Feature: Paste too few rows into sheet

  Scenario: Pasting a valid row into the edit forecast table
    Given the user selects all rows in the edit forecast table
     When the user pastes valid row data
     Then the too few rows error is displayed
