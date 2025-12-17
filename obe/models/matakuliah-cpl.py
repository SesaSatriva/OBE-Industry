from odoo import models, fields, api

class MataKuliahCpl(models.Model):
    _name = 'obe.mata.kuliah.cpl'
    _description = 'Mapping CPL per Mata Kuliah'

    mata_kuliah_id = fields.Many2one(
        'obe.mata.kuliah',
        ondelete='cascade',
        required=True
    )

    cpl_id = fields.Many2one(
        'obe.cpl',
        required=True
    )

    nilai = fields.Float(string='Bobot (%)')
