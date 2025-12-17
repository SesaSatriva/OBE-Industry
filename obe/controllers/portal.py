from odoo import http
from odoo.http import request
# import json


class OBEPortal(http.Controller):

    @http.route('/my/obe', type='http', auth='user', website=True)
    def portal_obe_dashboard(self):
        user = request.env.user
        Mahasiswa = request.env['obe.mahasiswa'].sudo()

        mahasiswa = Mahasiswa.search([
            ('user_id', '=', user.id)
        ], limit=1)

        if not mahasiswa:
            return request.render('obe.portal_obe_dashboard', {
                'mahasiswa': False
            })

        nilai_list = mahasiswa.nilai_ids

        # ===== RINGKASAN AKADEMIK =====
        mk_ids = nilai_list.mapped('mata_kuliah_id')
        avg_nilai = (
            round(sum(nilai_list.mapped('nilai')) / len(nilai_list), 2)
            if nilai_list else 0
        )

        # ===== CPL ACHIEVEMENT =====
        cpl_stat = {}

        for nilai in nilai_list:
            cpmk = nilai.cpmk_id
            cpl = cpmk.cpl_id if cpmk else False
            if not cpl:
                continue

            cpl_stat.setdefault(cpl.id, {
                'name': cpl.name,
                'total': 0,
                'pass': 0,
            })

            cpl_stat[cpl.id]['total'] += 1
            if nilai.nilai >= 75:
                cpl_stat[cpl.id]['pass'] += 1

        cpl_labels = []
        cpl_values = []

        for data in cpl_stat.values():
            percent = round(
                (data['pass'] / data['total']) * 100, 2
            ) if data['total'] else 0

            cpl_labels.append(data['name'])
            cpl_values.append(percent)

        summary = {
            'mk_count': len(mk_ids),
            'avg_nilai': avg_nilai,
            'cpl_percent': round(
                sum(cpl_values) / len(cpl_values), 2
            ) if cpl_values else 0,
        }

        return request.render('obe.portal_obe_dashboard', {
            'mahasiswa': mahasiswa,
            'nilai_list': nilai_list,
            'summary': summary,

            # # OWL + Chart.js friendly
            # 'cpl_chart_data': json.dumps({
            #     'labels': cpl_labels,
            #     'values': cpl_values,
            # }),
        })
