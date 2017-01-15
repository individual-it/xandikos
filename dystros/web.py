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

"""Web server implementation..

This is the concrete web server implementation. It provides the
high level application logic that combines the WebDAV server,
the carddav support, the caldav support and the DAV store.
"""

from dystros import caldav, carddav, webdav

WELLKNOWN_DAV_PATHS = set([caldav.WELLKNOWN_CALDAV_PATH, carddav.WELLKNOWN_CARDDAV_PATH])
CALENDAR_HOME_SET = '/user/calendars/'
ADDRESSBOOK_HOME_SET = '/user/contacts/'
CURRENT_USER_PRINCIPAL = '/user/'


class CalendarResource(webdav.DAVCollection):

    resource_types = webdav.DAVCollection.resource_types + [caldav.CALENDAR_RESOURCE_TYPE]

    def get_displayname(self):
        return "A calendar resource"


class AddressbookResource(webdav.DAVCollection):

    resource_types = webdav.DAVCollection.resource_types + [carddav.ADDRESSBOOK_RESOURCE_TYPE]

    def get_displayname(self):
        return "An addressbook resource"


class CalendarSetResource(webdav.DAVCollection):
    """Resource for calendar sets."""

    def members(self):
        return [('foo', CalendarResource())]


class AddressbookSetResource(webdav.DAVCollection):
    """Resource for addressbook sets."""

    def members(self):
        return [('foo', AddressbookResource())]


class UserPrincipalResource(webdav.DAVCollection):
    """Principal user resource."""

    resource_types = webdav.DAVCollection.resource_types + ['{DAV:}principal']

    def members(self):
        return [('calendars', CalendarSetResource())]


class DystrosBackend(webdav.DAVBackend):

    def get_resource(self, p):
        if p in WELLKNOWN_DAV_PATHS:
            return webdav.WellknownResource("/")
        elif p == "/":
            return webdav.NonDAVResource()
        elif p == CURRENT_USER_PRINCIPAL:
            return UserPrincipalResource()
        elif p == CALENDAR_HOME_SET:
            return CalendarSetResource()
        elif p == ADDRESSBOOK_HOME_SET:
            return AddressbookSetResource()
        elif p == ADDRESSBOOK_HOME_SET + 'foo/':
            return AddressbookResource()
        elif p == CALENDAR_HOME_SET + 'foo/':
            return CalendarResource()
        else:
            return None


class DystrosApp(webdav.WebDAVApp):
    """A wsgi App that provides a Dystros web server.
    """

    def __init__(self):
        super(DystrosApp, self).__init__(DystrosBackend())
        self.register_properties([
            webdav.DAVResourceTypeProperty(),
            webdav.DAVCurrentUserPrincipalProperty(CURRENT_USER_PRINCIPAL),
            webdav.DAVDisplayNameProperty(),
            caldav.CalendarHomeSetProperty(CALENDAR_HOME_SET),
            carddav.AddressbookHomeSetProperty(ADDRESSBOOK_HOME_SET),
            ])


if __name__ == '__main__':
    import optparse
    import sys
    parser = optparse.OptionParser()
    parser.add_option("-l", "--listen_address", dest="listen_address",
                      default="localhost",
                      help="Binding IP address.")
    parser.add_option("-p", "--port", dest="port", type=int,
                      default=8000,
                      help="Port to listen on.")
    options, args = parser.parse_args(sys.argv)

    from wsgiref.simple_server import make_server
    app = DystrosApp()
    server = make_server(options.listen_address, options.port, app)
    server.serve_forever()
