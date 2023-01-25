# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Vendor views, w/ Quickbooks integration
"""

from tailbone.views import ViewSupplement


class VendorViewSupplement(ViewSupplement):
    """
    Vendor view supplement for Quickbooks integration
    """
    route_prefix = 'vendors'

    def get_grid_query(self, query):
        model = self.model
        return query.outerjoin(model.QuickbooksVendor)

    def configure_grid(self, g):
        model = self.model
        g.set_filter('quickbooks_name', model.QuickbooksVendor.quickbooks_name)
        g.set_filter('quickbooks_bank_account', model.QuickbooksVendor.quickbooks_bank_account)
        g.set_filter('quickbooks_terms', model.QuickbooksVendor.quickbooks_terms)

    def configure_form(self, f):
        f.append('quickbooks_name')
        f.append('quickbooks_bank_account')
        f.append('quickbooks_terms')

    def get_version_child_classes(self):
        model = self.model
        return [model.QuickbooksVendor]


def includeme(config):
    VendorViewSupplement.defaults(config)
