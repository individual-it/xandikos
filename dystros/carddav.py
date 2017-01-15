# Dystros
# Copyright (C) 2016 Jelmer Vernooij <jelmer@jelmer.uk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your option) any later version of
# the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""CardDAV support.

https://tools.ietf.org/html/rfc6352
"""
import defusedxml.ElementTree
from xml.etree import ElementTree as ET

from dystros import webdav

WELLKNOWN_CARDDAV_PATH = "/.well-known/carddav"

NAMESPACE = 'urn:ietf:params:xml:ns:carddav'
ADDRESSBOOK_RESOURCE_TYPE = '{%s}addressbook' % NAMESPACE


class AddressbookHomeSetProperty(webdav.DAVProperty):
    """addressbook-home-set property

    See https://tools.ietf.org/html/rfc6352, section 7.1.1
    """

    name = '{%s}addressbook-home-set' % NAMESPACE
    in_allprops = False

    def __init__(self, addressbook_home_set):
        super(AddressbookHomeSetProperty, self).__init__()
        self.addressbook_home_set = addressbook_home_set

    def populate(self, resource, el):
        ET.SubElement(el, '{DAV:}href').text = self.addressbook_home_set
