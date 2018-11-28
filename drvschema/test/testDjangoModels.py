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
import os
import shutil
import drvschema
import subprocess


TEST_PROJECT_PATH = os.path.join(os.path.dirname(__file__), 'drv')
TEST_PROJECT_MODEL_PATH = os.path.join(TEST_PROJECT_PATH, 'drv', 'models.py')


def cleanTestProject():
    """
    Removes migrations and sqlite db for the drv test Django project
    """
    if not os.path.exists(TEST_PROJECT_PATH):
        raise Exception('Test project %s does not exist!' % TEST_PROJECT_PATH)

    try:
        os.unlink(os.path.join(TEST_PROJECT_PATH, 'drv', 'migrations', '0001_initial.py'))
        os.unlink(os.path.join(TEST_PROJECT_PATH, 'db.sqlite3'))
        os.unlink(TEST_PROJECT_MODEL_PATH)
    except Exception as e:
        # sys.stderr.print("Failure to remove migrations and sqlitedb: %s" % str(e))
        pass


class TestDjangoModels(unittest.TestCase):

    def setUp(self):
        cleanTestProject()

    def tearDown(self):
        cleanTestProject()

    def testCharFieldKwargs(self):
        """
        Ensure that Django model CharField kwargs are correctly created
        """
        appschema = drvschema.DrvSchema({
            'User': {
                'first_name': {
                    'required': True,
                    'maxlength': 200,
                    'help': 'User first name',
                },
            }
        })

        kwargs = appschema.to('DjangoModelCharFieldKwargs', 'User.first_name')
        self.assertTrue(kwargs['max_length'] == 200)
        self.assertTrue(kwargs['help_text'] == 'User first name')
        self.assertFalse(kwargs['blank'])
        self.assertTrue(kwargs['default'] is None)
        self.assertTrue('required' not in kwargs)

    def testMigration(self):
        """
        Do an actual migration with a Django model (drv project)
        """
        modelstext = r'''
from django.db import models
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

class Test(models.Model):
    name = models.CharField(**APPSCHEMA.to('DjangoModelCharFieldKwargs', 'Test.name'))
    description = models.CharField(**APPSCHEMA.to('DjangoModelCharFieldKwargs', 'Test.description'))
        '''
        with open(TEST_PROJECT_MODEL_PATH, 'w') as f:
            f.write(modelstext)

        cmd = './manage.py makemigrations drv && ./manage.py migrate'
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, cwd=TEST_PROJECT_PATH)
        stdoutstr, stderrstr = proc.communicate()
        self.assertTrue(proc.returncode == 0, "Migration failed: \n%s\n%s" % (stdoutstr, stderrstr))
