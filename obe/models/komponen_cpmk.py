from odoo import models, fields, api
from odoo.exceptions import ValidationError


class KomponenCpmk(models.Model):
    _name = 'obe.komponen.cpmk'
    _description = 'Distribusi Komponen ke CPMK Kelas'

    komponen_id = fields.Many2one(
        'obe.komponen.penilaian',
        required=True,
        ondelete='cascade'
    )

    cpmk_kelas_id = fields.Many2one(
        'obe.cpmk.kelas',
        required=True,
        ondelete='cascade'
    )

    bobot = fields.Float(
        string='Bobot CPMK (%)',
        required=True
    )

    _sql_constraints = [
        (
            'unique_komponen_cpmk',
            'unique(komponen_id, cpmk_kelas_id)',
            'Komponen tidak boleh dipetakan dua kali ke CPMK yang sama.'
        )
    ]
