from __future__ import print_function
import os
import simplejson as json

from django.conf import settings as django_settings
from django.core.management.base import BaseCommand

from tendenci.apps.site_settings.models import Setting


class Command(BaseCommand):
    """
    Update site settings in the database. It reads the settings.json
    under each installed app or apps specified in the arguments,
    and add or update the settings accordingly.

    Usage:
        python manage.py update_settings <appname appname ...>

    Example:
        python manage.py update_settings articles plugins.donations

    If no appname specified, it updates for ALL installed apps.

    Json required fields (for lookups):
        `scope`
        `scope_category`
        `name`

    Json columns that cannot be updated:
        `value`: It would just be mean to override a
                 clients setting value

    Json format:
        [
          {
            "name": "",
            "label": "",
            "description": "",
            "data_type": "",
            "default_value": "",
            "input_type": "",
            "input_value": "",
            "client_editable": "",
            "store": "",
            "scope": "",
            "scope_category": "",
          }
        ]

    Json example:
        [
          {
            "name": "enabled",
            "label": "enabled",
            "description": "Module is enabled or not.",
            "data_type": "boolean",
            "default_value": "true",
            "input_type": "select",
            "input_value": "true, false",
            "client_editable": "1",
            "store": "1",
            "scope": "module",
            "scope_category": "memberships",
          }
        ]

    Json field definitions:
        `name`: The machine name. No spaces or special characters.
              Remember that this is what the python code uses to
              find the setting

        `label`: The human readable version of 'name'

        `description`: A non-html or html description of the setting.
                       Refer to the 'site_settings_setting' table for examples

        `data_type`: boolean or string

        `default_value`: the original value

        `input_type`: select or text (used by the autogenerated interface)

        `input_value`: comma delimited list or just a string

        `store`: boolean value. Tell the system whether or not to
               cache the setting

        `scope`: site or module

        `scope_category`: this is the module name the settings belongs too.
                        refer to django contenttypes app_label. If this
                        is a settings that doesn't apply to a django
                        application use 'global'
    """
    help = 'Update settings in the site_settings_setting table'

    def update_settings(self, settings, verbosity=1):
        """
        Loop through the settings and add or update them
        """
        required_keys = [
            'scope',
            'scope_category',
            'name'
        ]
        for setting in settings:
            # check the required fields
            req_list = [k for k in setting.keys() if k in required_keys]
            if len(req_list) != len(required_keys):
                print('Setting does not have the required fields ... skipping.')
                continue

            try:
                current_setting = Setting.objects.filter(**{
                    'name': setting['name'],
                    'scope': setting['scope'],
                    'scope_category': setting['scope_category']
                })[0]
            except:
                current_setting = None

            # update the setting
            if (current_setting):
                # skip the value for the existing setting
                if 'value' in setting:
                    del setting['value']
                current_setting.__dict__.update(setting)
                current_setting.save()
                print('%s (%s)  - updated.' % (
                    setting['name'],
                    setting['scope_category']
                ))
            else:
                # insert
                new_setting = Setting(**setting)
                new_setting.save()
                #if verbosity >= 2:
                print('%s (%s)  - added.' % (
                    setting['name'],
                    setting['scope_category']
                ))

    def add_arguments(self, parser):
        # optional arguments
        parser.add_argument('appnames',
            nargs='*',
            help='app names to update')

    def handle(self, appnames, **options):
        try:
            verbosity = int(options['verbosity'])
        except:
            verbosity = 1

        if not appnames:
            appnames = django_settings.INSTALLED_APPS
            # exclude django native apps
            appnames = [app for app in appnames if not app.startswith('django.')]

        for appname in appnames:
            print()
            print('Processing for %s ...' % appname)
            if appname.startswith('addons.') or appname.startswith('themes.'):
                json_file = os.path.abspath(os.path.join(
                                django_settings.PROJECT_ROOT,
                                '/'.join(appname.split('.')),
                                'settings.json'
                            ))
            else:
                if appname.find('.') != -1:
                    appname = appname.replace('.', '/')
                json_file = os.path.abspath(os.path.join(
                                django_settings.TENDENCI_ROOT,'..',
                                '/'.join(appname.split('.')),
                                'settings.json'
                            ))
            if os.path.isfile(json_file):
                with open(json_file, 'r') as f:
                    try:
                        settings = json.loads(f.read())
                    except ValueError as e:
                        print("Error updating setting for %s/settings.json" % appname)
                        print(e)
                        continue

                if settings:
                    self.update_settings(settings, verbosity=verbosity)
