*** Settings ***
Documentation    Utility keywords for the e2e tests.

Library          RequestsLibrary
Library          Collections
Library          String
Library          Browser

Variables        ../variables.py

*** Keywords ***
Select Option By
    [Documentation]    Selects an option from a custom select component (non-native)
    [Arguments]    ${trigger_locator}    ${option_value}
    Click    ${trigger_locator}
    Click    [role=option]:has-text("${option_value}")