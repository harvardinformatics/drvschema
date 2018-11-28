# -*- coding: utf-8 -*-

'''
DrvSchema class

Provides a convenient interface for converting Cerberus schema definitions into tools and stuff.


from drvschema import DrvSchema

APPSCHEMA = DrvSchema({
    'User': {
        'first_name': {
            'type': 'string',
            'maxlength': 200,
            'required': True,
        },
        'last_name': {
            'type': 'string',
            'maxlength': 200,
            'required': True,
        },
        'email': {
            'type': 'string',
            'maxlength': 100,
            'validator': emailValidator,
        }
    }
})

class User:
    first_name = models.CharField(**APPSCHEMA.to('DjangoModelCharFieldKwargs', 'User.first_name'))
    last_name = models.CharField(**APPSCHEMA.to('DjangoModelCharFieldKwargs', 'User.last_name'))
    email = models.CharField(**APPSCHEMA.to('DjangoModelCharFieldKwargs', 'User.email'))


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(**APPSCHEMA.to('DRFSerializerCharFieldKwargs', 'User.first_name'))
    last_name = serializers.CharField(**APPSCHEMA.to('DRFSerializerCharFieldKwargs', 'User.last_name'))
    email = serializers.CharField(**APPSCHEMA.to('DRFSerializerCharFieldKwargs', 'User.email'))

class UserForm(forms.ModelForm)
    first_name = forms.CharField(**APPSCHEMA.to('DjangoFormCharFieldKwargs', 'User.first_name'))
    last_name = forms.CharField(**APPSCHEMA.to('DjangoFormCharFieldKwargs', 'User.last_name'))
    email = forms.CharField(**APPSCHEMA.to('DjangoFormCharFieldKwargs', 'User.email'))

>>> print(APPSCHEMA.to('VuelidateValidations', 'User'))
first_name: {
    required,
    maxLength: maxLength(200)
},
last_name: {
    required,
    maxLength: maxLength(200)
},
email: {
    email
}
>>>


Created on  2018-11-27

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2018 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from drvschema import converter


class DrvSchema:
    """
    DrvSchema class that provides the interface for interacting with the schema

    Uses a Cerberus (https://pypi.org/project/Cerberus/) schema and a set of converters
    that will create arguments or representations for different purposes.
    """
    def __init__(self, schemata, converters={}):
        """
        Takes a list of Cerberus schema dictionaries keyed by class name and field name
        """
        self.schemata = schemata
        if len(converters) == 0:
            self.converters = {
                'DjangoModelCharFieldKwargs': converter.DjangoModelCharFieldKwargs,
                'DjangoModelBooleanFieldKwargs': converter.DjangoModelBooleanFieldKwargs,
                'DjangoModelDateTimeFieldKwargs': converter.DjangoModelDateTimeFieldKwargs,
                'DjangoModelForeignKeyFieldKwargs': converter.DjangoModelForeignKeyFieldKwargs,
                'DRFSerializerCharFieldKwargs': converter.DRFSerializerCharFieldKwargs,
                'VuelidateValidations': converter.VuelidateValidations,
            }

    def to(self, converter_name, keystr):
        """
        Use the specified converter and key string to convert the corresponding schema element
        Converter name must be in the converter list
        """
        if converter_name not in self.converters:
            raise Exception('DrvSchema was not initialized with converter %s' % converter_name)

        f = self.converters[converter_name]

        return f(self.schemata, keystr)
