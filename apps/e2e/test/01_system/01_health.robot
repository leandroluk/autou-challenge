*** Settings ***
Documentation       E2E tests for the Control API system health status.

Resource            ../../resource/util.resource

Suite Setup         Setup Test Suite
Suite Teardown      Teardown Test Suite


*** Variables ***
${HEALTH_PATH}      /api/v1/system/health


*** Test Cases ***
Verify API System Health Status
    [Documentation]    Verify API system health status
    ${json}=    Do System Health Request
    Validate System Health Request    ${json}


*** Keywords ***
Setup Test Suite
    [Documentation]    Initializes API session and cleans IMAP inbox
    Create Session    session    ${API_BASE_URL}    verify=True

Teardown Test Suite
    [Documentation]    Closes all sessions
    Delete All Sessions

Do System Health Request
    [Documentation]    Performs the health check request and returns the JSON body
    ${response}=    GET On Session    session    ${HEALTH_PATH}    expected_status=200
    RETURN    ${response.json()}

Validate System Health Request
    [Documentation]    Validates the main health keys
    [Arguments]    ${json}
    Dictionary Should Contain Key    ${json}    uptime
    Should Not Be Empty    ${json}[uptime]    msg=Uptime report is empty
