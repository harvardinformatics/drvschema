# -*- coding: utf-8 -*-

'''
testDrfSerializers

Test for Django Rest Framework Serializers

Created on  2018-11-27

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2018 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import unittest
from drvschema import DrvSchema


class TestDrfSerializers(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCharFieldKwargs(self):
        """
        Make sure DRF Serializer CharField kwargs are properly created.  Just testing expected text.
        """
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
                    'empty': True,
                    'readonly': True,
                }
            }
        })

        kwargs = APPSCHEMA.to('DRFSerializerCharFieldKwargs', 'Test.name')

        self.assertTrue(kwargs['required'])
        self.assertTrue(kwargs['max_length'] == 100)
        self.assertTrue('empty' not in kwargs)
        self.assertTrue('default' not in kwargs)
        self.assertTrue('read_only' not in kwargs)

        kwargs = APPSCHEMA.to('DRFSerializerCharFieldKwargs', 'Test.description')
        self.assertTrue(kwargs['read_only'])
        self.assertFalse(kwargs['required'])
