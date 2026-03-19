*** Settings ***
Documentation       E2E tests for the email analyze endpoint.

Resource            ../../resource/util.resource

Suite Setup         Setup Test Suite
Suite Teardown      Teardown Test Suite


*** Variables ***
${EMAIL_FILE_PDF_PATH}      ${CURDIR}/../../resource/email.pdf
${EMAIL_FILE_TXT_PATH}      ${CURDIR}/../../resource/email.txt
${EMAIL_TEXT_CONTENT}       Subject: Test\n\nThis is a test email body.
${EMAIL_ANALYZE_PATH}       /api/v1/email/analyze


*** Test Cases ***
Verify API Email Analyze With Text
    [Documentation]    Analyze email using plain text
    ${json}=    Do Email Analyze Request With Text    ${EMAIL_TEXT_CONTENT}
    Validate Email Analyze Response    ${json}

Verify API Email Analyze With PDF File
    [Documentation]    Analyze email using PDF file
    ${json}=    Do Email Analyze Request With File    ${EMAIL_FILE_PDF_PATH}    "application/pdf"
    Validate Email Analyze Response    ${json}

Verify API Email Analyze With TXT File
    [Documentation]    Analyze email using TXT file
    ${json}=    Do Email Analyze Request With File    ${EMAIL_FILE_TXT_PATH}    "text/plain"
    Validate Email Analyze Response    ${json}


*** Keywords ***
Setup Test Suite
    [Documentation]    Initializes API session
    Create Session    session    ${API_BASE_URL}    verify=True

Teardown Test Suite
    [Documentation]    Closes all sessions
    Delete All Sessions

Do Email Analyze Request With Text
    [Documentation]    Sends email analyze request using text
    [Arguments]    ${text}
    VAR    &{data}=    provider=${EMAIL_ANALYSIS_PROVIDER}    api_key=${GEMINI_API_KEY}    text=${text}
    ${response}=    POST On Session    session    ${EMAIL_ANALYZE_PATH}    data=${data}
    RETURN    ${response.json()}

Do Email Analyze Request With File
    [Documentation]    Sends email analyze request using file
    [Arguments]    ${file_path}    ${mime_type}
    VAR    &{data}=    provider=${EMAIL_ANALYSIS_PROVIDER}    api_key=${GEMINI_API_KEY}
    ${file_tuple}=    Evaluate    ("file", open($file_path, "rb"), $mime_type)
    VAR    &{files}=    file=${file_tuple}
    ${response}=    POST On Session    session    ${EMAIL_ANALYZE_PATH}    data=${data}    files=${files}
    RETURN    ${response.json()}

Validate Email Analyze Response
    [Documentation]    Validates the email analyze response keys
    [Arguments]    ${json}
    Dictionary Should Contain Key    ${json}    category
    Dictionary Should Contain Key    ${json}    reply
    Should Not Be Empty    ${json}[category]    msg=Category is empty
    Should Not Be Empty    ${json}[reply]    msg=Reply is empty
