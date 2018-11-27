
from drvschema import DrvSchema

APPSCHEMA = DrvSchema({
    'Test': {
        'name': {
            'required': True,
            'maxlength': 100,
            'empty': False,
            'default': None,
        },
        'description': {
            'required': False,
            'maxlength': 255,
            'empty': True
        }
    }
})
