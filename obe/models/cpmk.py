from odoo import models, fields, api


class Cpmk(models.Model):
    _name = 'obe.cpmk'
    _description = 'Capaian Pembelajaran Mata Kuliah'

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Kode CPMK harus unik!')
    ]

    code = fields.Char(string='Kode CPMK', required=True)
    description = fields.Text(string='Deskripsi CPMK', required=True)
    bobot = fields.Float(string='Bobot CPMK', required=True)

    mata_kuliah_id = fields.Many2one(
        comodel_name='obe.mata.kuliah',
        string='Mata Kuliah',
        required=True,
        ondelete='cascade'
    )

    cpl_ids = fields.Many2many(
        comodel_name='obe.cpl',
        relation='obe_cpl_cpmk_rel',
        column1='cpmk_id',
        column2='cpl_id',
        string='CPL Terkait'
    )

    def name_get(self):
        return [(rec.id, f"{rec.code} - {rec.mata_kuliah_id.kode}") for rec in self]
