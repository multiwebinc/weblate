# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2013 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from trans.machine.base import MachineTranslation
from django.core.exceptions import ImproperlyConfigured
from weblate.appsettings import MT_TMSERVER
import urllib


class TMServerTranslation(MachineTranslation):
    '''
    tmserver machine translation support.
    '''
    name = 'tmserver'

    def __init__(self):
        '''
        Checks configuration.
        '''
        super(TMServerTranslation, self).__init__()
        self.url = self.get_server_url()

    def get_server_url(self):
        '''
        Returns URL of a server.
        '''
        if MT_TMSERVER is None:
            raise ImproperlyConfigured(
                'Not configured tmserver URL'
            )

        return MT_TMSERVER.rstrip('/')

    def convert_language(self, language):
        '''
        Converts language to service specific code.
        '''
        return language.replace('-', '_').lower()

    def is_supported(self, language):
        '''
        Any language is supported.
        '''
        return True

    def download_translations(self, language, text, unit):
        '''
        Downloads list of possible translations from a service.
        '''
        url = '%s/tmserver/en/%s/unit/%s' % (
            self.url,
            urllib.quote(language),
            urllib.quote(text.encode('utf-8')),
        )
        response = self.json_req(url)

        return [(line['target'], line['quality'], self.name, line['source'])
                for line in response]


class AmagamaTranslation(TMServerTranslation):
    '''
    Specific instance of tmserver ran by Virtaal authors.
    '''
    name = 'Amagama'

    def get_server_url(self):
        return 'http://amagama.locamotion.org'
