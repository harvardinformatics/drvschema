# -*- coding: utf-8 -*-

'''
testDjangoModels

Test for Django model field kwargs

Created on  2018-11-27

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2018 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import unittest
from drvschema import DrvSchema


class testDjangoModels(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCharFieldKwargs(self):
        """
        Ensure that Django model CharField kwargs are correctly created
        """
        appschema = DrvSchema({
            'User': {
                'first_name': {
                    'required': True,
                    'maxlength': 200,
                    'help': 'User first name',
                    'empty': False,
                    'default': None,
                },
            }
        })

        kwargs = appschema.to('DjangoModelCharFieldKwargs', 'User.first_name')
        self.assertTrue(kwargs['required'])
        self.assertTrue(kwargs['max_length'] == 200)
        self.assertTrue(kwargs['help_text'] == 'User first name')
        self.assertFalse(kwargs['blank'])
        self.assertTrue(kwargs['default'] is None)
