from odoo import http
from odoo.http import request


class PortalRedirect(http.Controller):

    @http.route(['/my'], type='http', auth='user', website=True)
    def portal_my_redirect(self, **kw):
        Mahasiswa = request.env['obe.mahasiswa'].sudo()

        mahasiswa = Mahasiswa.search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)

        if mahasiswa:
            return request.redirect('/my/obe')

        return request.render('portal.portal_my_home')
