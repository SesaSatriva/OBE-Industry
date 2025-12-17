from odoo import models, fields, api
class NilaiCpmk(models.Model):
    _name = 'obe.nilai.cpmk'
    _description = 'Nilai CPMK Mahasiswa'

    _sql_constraints = [
        (
            'unique_mahasiswa_cpmk',
            'unique(mahasiswa_id, cpmk_id)',
            'Nilai CPMK mahasiswa harus unik!'
        )
    ]

    mahasiswa_id = fields.Many2one(
        'obe.mahasiswa', string='Mahasiswa', required=True, ondelete='cascade'
    )
    cpmk_id = fields.Many2one(
        'obe.cpmk', string='CPMK', required=True, ondelete='cascade'
    )

    nilai = fields.Float(string='Nilai', required=True)
