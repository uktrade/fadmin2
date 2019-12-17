Feature: Paste too many rows into sheet

  Scenario: Pasting a valid row into the edit forecast table
    Given the user selects all rows in the edit forecast table
     When the user pastes too many rows
     Then the too many rows error is displayed
