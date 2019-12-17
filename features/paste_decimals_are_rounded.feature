Feature: On pasting row, decimals are rounded

  Scenario: Pasting a valid row into the edit forecast table
    Given the user selects a row in the edit forecast table
     When the user pastes valid row data with a 5 decimal place value
     Then the clipboard data is displayed in the forecast table
     And the stored value has been rounded correctly
