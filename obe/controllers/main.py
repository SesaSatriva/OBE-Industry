from odoo import http
from odoo.http import request

class OBEWebsite(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def obe_homepage(self):
        return request.render('obe.obe_homepage')

    @http.route('/profil-prodi', type='http', auth='public', website=True)
    def profil_prodi(self):
        prodi = request.env['program.studi'].sudo().search(
            [('is_published', '=', True)],
            limit=1
        )
        return request.render(
            'obe.page_profil_prodi',
            {'prodi': prodi}
        )
    
    @http.route('/cpl', type='http', auth='public', website=True)
    def cpl_public(self):
        cpls = request.env['obe.cpl'].sudo().search([], order='cpl_ids')
        return request.render(
            'obe.page_cpl_public',
            {'cpls': cpls}
        )

