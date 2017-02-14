# Xandikos
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

"""WSGI wrapper for xandikos.
"""

import os

from xandikos.web import XandikosApp

from prometheus_client import multiprocess
from prometheus_client import CollectorRegistry, make_wsgi_app


app = XandikosApp(
        path=os.environ['XANDIKOSPATH'],
        current_user_principal=os.environ.get('CURRENT_USER_PRINCIPAL', '/user/'))

if os.environ.get('ENABLE_PROMETHEUS', '1') == '1':
    from xandikos.prometheus import PrometheusRedirector, DEFAULT_PROMETHEUS_DIR
    prometheus_dir = os.environ.get('PROMETHEUS_DIR', DEFAULT_PROMETHEUS_DIR)
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry, os.prometheus_dir)
    app_with_metrics = PrometheusRedirector(app, registry)
