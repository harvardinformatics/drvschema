# -*- coding: utf-8 -*-

'''
drvschema.converter

module containing converters.

Converters are functions that take a schemata, and a key list and return the needed validation code.
The key list is used to interrogate the schemata

Created on  2018-11-27

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2018 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from collections import defaultdict
import json
import re


def getSchemaFromKeys(schemata, keystr):
    """
    Split the key string and retrieve the appropriate data
    from the schemata by iterating through the key elements in order
    """
    keys = keystr.split('.')
    schema = schemata
    for key in keys:
        if key in schema:
            schema = schema[key]
        else:
            raise Exception('Key %s from keys %s cannot be found in the schemata.' % (key, ','.join(keys)))

    return schema


def DjangoModelCharFieldKwargs(schemata, keystr):
    """
    Convert a schema to Django model CharField arguments using schemata and key string
    """
    schema = getSchemaFromKeys(schemata, keystr)
    kwargs = {}

    # Map of schema keys to CharField kwarg keys
    fieldmap = {
        'maxlength': 'max_length',
        'help': 'help_text',
        'empty': 'blank',
        'default': 'default',
        'unique': 'unique',
        'nullable': 'null',
    }

    for k, v in fieldmap.items():
        if k in schema:
            kwargs[v] = schema[k]

    if 'required' in schema:
        kwargs['blank'] = False
        kwargs['default'] = None
        kwargs['null'] = False

    return kwargs


def DRFSerializerCharFieldKwargs(schemata, keystr):
    """
    Convert a schema to Django Rest Framework CharField arguments
    """
    schema = getSchemaFromKeys(schemata, keystr)
    kwargs = {}

    # Map of schema keys to CharField kwarg keys
    fieldmap = {
        'maxlength': 'max_length',
        'help': 'help_text',
        'required': 'required',
        'readonly': 'read_only',
    }

    for k, v in fieldmap.items():
        if k in schema:
            kwargs[v] = schema[k]

    return kwargs


def VuelidateValidations(schemata, keystr):
    """
    Convert a schema into Vuelidate validations JSON.
    Generally this will be done against each type and the results will
    be pasted into the Vue code.
    """
    schemadict = getSchemaFromKeys(schemata, keystr)
    result = defaultdict(dict)
    for field, schema in schemadict.items():
        if 'required' in schema and schema['required']:
            result[field]['required'] = ''
        if 'maxlength' in schema:
            result[field]['maxLength'] = 'maxLength(%d)' % schema['maxlength']

    resultstr = json.dumps(result)

    # Strip the quotes from maxLength because it's a function
    resultstr = re.sub(r'"(maxLength\(\d+\))"', r'\1', resultstr)

    return resultstr
