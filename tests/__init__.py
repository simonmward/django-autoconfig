'''Tests for django-autoconfig.'''
# pylint: disable=C0103
# pylint: disable=R0904

from django_autoconfig import autoconfig

import copy
try:
    from django.utils import unittest
except ImportError:
    import unittest

import logging
LOGGER = logging.getLogger(__name__)

class ConfigureSettingsTestCase(unittest.TestCase):
    '''Test the configure_settings method.'''

    BASE_SETTINGS = {
        'LIST_SETTING': [1, 2],
        'BOOLEAN_SETTING': True,
        'DICT_SETTING': {
            'key1': 'value1',
        },
    }

    def setUp(self):
        self.settings = copy.deepcopy(self.BASE_SETTINGS)

    def test_list_merging(self):
        '''
        Test that list settings are merged correctly
        '''

        self.settings['INSTALLED_APPS'] = ['tests.app_list']
        autoconfig.configure_settings(self.settings)
        self.assertEqual(self.settings['LIST_SETTING'], [1, 2, 3])

    def test_new_setting(self):
        '''
        A new setting (i.e. not in the DJANGO_SETTINGS_MODULE)
        should just end up as the new value.
        '''
        self.settings['INSTALLED_APPS'] = ['tests.app_new_setting']
        autoconfig.configure_settings(self.settings)
        self.assertEqual(self.settings['NEW_LIST_SETTING'], [1, 2, 3])

    def test_list_setting_from_defaults(self):
        '''
        A list setting that exists in the django.conf.settings.global_settings
        should merge with the default, not replace it entirely.
        '''
        self.settings['INSTALLED_APPS'] = ['tests.app_middleware']
        autoconfig.configure_settings(self.settings)
        self.assertIn('my.middleware', self.settings['MIDDLEWARE_CLASSES'])
        self.assertIn('django.middleware.common.CommonMiddleware', self.settings['MIDDLEWARE_CLASSES'])