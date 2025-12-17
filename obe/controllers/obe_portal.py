from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

class OBEPortalMenu(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        values['portal_docs'].append({
            'title': 'Portal OBE Mahasiswa',
            'url': '/my/obe',
            'icon': 'graduation-cap',
        })

        return values
