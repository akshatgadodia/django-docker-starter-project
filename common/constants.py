TITLE = 'Backend'
INDEX_PAGE_TITLE = 'Dashboard'
DESCRIPTION = 'This is a backend project'
CURRENT_VERSION = 'v1'
CONTACT_EMAIL = 'example@example.com'
TERMS_URL = "https://example.com/"
PROJECT_LICENSE_NAME ="BSD License"

SUCCESS = True
FAILED = False

DEFAULT_SINGLETON_INSTANCE_ID = 1

TRUE_VALUES = {
    't', 'T',
    'y', 'Y', 'yes', 'Yes', 'YES',
    'true', 'True', 'TRUE',
    'on', 'On', 'ON',
    '1', 1,
    True
}
FALSE_VALUES = {
    'f', 'F',
    'n', 'N', 'no', 'No', 'NO',
    'false', 'False', 'FALSE',
    'off', 'Off', 'OFF',
    '0', 0, 0.0,
    False
}
NULL_VALUES = {'null', 'Null', 'NULL', '', None}