from odoo import models, fields

class Cpl(models.Model):
    _name = 'obe.cpl'
    _description = 'Capaian Pembelajaran Lulusan'

    _sql_constraints = [
        ('cpl_ids_unique', 'unique(cpl_ids)', 'Kode CPL harus unik!')
    ]

    cpl_ids = fields.Char(string='Kode CPL', required=True)
    description = fields.Text(string='Deskripsi', required=True)
    bobot = fields.Float(string='Bobot (%)')

    cpmk_ids = fields.Many2many(
        'obe.cpmk',
        relation='obe_cpl_cpmk_rel',
        column1='cpl_id',
        column2='cpmk_id',
        string='CPMK'
    )

    dosen_ids = fields.Many2many(
        'obe.dosen',
        relation='obe_dosen_cpl_rel',
        column1='cpl_id',
        column2='dosen_id',
        string='Dosen Pengampu'
    )
    mata_kuliah_id = fields.Many2many(
        'obe.mata.kuliah',
        string='Mata Kuliah Terkait'
    )
