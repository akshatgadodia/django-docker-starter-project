# Swagger Settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'PERSIST_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'format': 'Bearer'
        }
    },
}