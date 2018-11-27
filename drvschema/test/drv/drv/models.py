# -*- coding: utf-8 -*-

'''
models for testing DrvSchema

Created on  2018-11-27

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2018 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from django.db import models
from drv import APPSCHEMA


class Test(models.Model):
    name = models.CharField(**APPSCHEMA.to('DjangoModelCharFieldKwargs', 'Test.name'))
    description = models.CharField(**APPSCHEMA.to('DjangoModelCharFieldKwargs', 'Test.description'))
