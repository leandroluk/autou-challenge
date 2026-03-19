*** Settings ***
Documentation       E2E tests for the email analyze UI.

Resource            ../../resource/util.resource

Suite Setup         Setup Test Suite
Suite Teardown      Teardown Test Suite


*** Variables ***
${EMAIL_FILE_PDF_PATH}      ${CURDIR}/../../resource/email.pdf
${EMAIL_FILE_TXT_PATH}      ${CURDIR}/../../resource/email.txt
${EMAIL_TEXT_CONTENT}       Subject: Test\n\nThis is a test email body.

${SEL_PROVIDER}             [data-testid=analysis-form_select_provider]
${SEL_API_KEY}              [data-testid=analysis-form_input_api-key]
${SEL_TAB_TEXT}             [data-testid=analysis-form_tab_text]
${SEL_TAB_FILE}             [data-testid=analysis-form_tab_file]
${SEL_TEXTAREA}             [data-testid=analysis-form_textarea_text]
${SEL_INPUT_FILE}           [data-testid=analysis-form_input_file]
${SEL_SUBMIT}               [data-testid=analysis-form_button_submit]


*** Test Cases ***
Verify Email Analyze With Text
    [Documentation]    Analyze email using plain text via UI
    Fill Provider Fields
    Click    ${SEL_TAB_TEXT}
    Fill Text    ${SEL_TEXTAREA}    ${EMAIL_TEXT_CONTENT}
    Click    ${SEL_SUBMIT}
    Wait For Elements State    text=Category    visible    timeout=30s

Verify Email Analyze With PDF File
    [Documentation]    Analyze email using PDF file via UI
    Fill Provider Fields
    Click    ${SEL_TAB_FILE}
    Upload File By Selector    ${SEL_INPUT_FILE}    ${EMAIL_FILE_PDF_PATH}
    Click    ${SEL_SUBMIT}
    Wait For Elements State    text=Category    visible    timeout=30s

Verify Email Analyze With TXT File
    [Documentation]    Analyze email using TXT file via UI
    Fill Provider Fields
    Click    ${SEL_TAB_FILE}
    Upload File By Selector    ${SEL_INPUT_FILE}    ${EMAIL_FILE_TXT_PATH}
    Click    ${SEL_SUBMIT}
    Wait For Elements State    text=Category    visible    timeout=30s


*** Keywords ***
Setup Test Suite
    [Documentation]    Opens browser and navigates to the app
    New Browser    chromium    headless=${HEADLESS}
    New Page    ${WEB_BASE_URL}

Teardown Test Suite
    [Documentation]    Closes browser
    Close Browser

Fill Provider Fields
    [Documentation]    Fills provider and API key fields
    Select Option By    ${SEL_PROVIDER}    ${EMAIL_ANALYSIS_PROVIDER}
    Fill Text    ${SEL_API_KEY}    ${GEMINI_API_KEY}