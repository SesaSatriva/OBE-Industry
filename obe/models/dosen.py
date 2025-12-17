from odoo import models, fields, api
class Dosen(models.Model):
    _name = 'obe.dosen'
    _description = 'Dosen'

    _sql_constraints = [
        ('nidn_unique', 'unique(nidn)', 'NIDN harus unik!')
    ]

    name = fields.Char(string='Nama', required=True)
    nidn = fields.Char(string='NIDN', required=True)
    email = fields.Char(string='Email')

    mahasiswa_ids = fields.One2many(
        comodel_name='obe.mahasiswa',
        inverse_name='dosen_pa_id',
        string='Mahasiswa Bimbingan'
    )

    mata_kuliah_id = fields.Many2many(
        comodel_name='obe.mata.kuliah',
        string='Mata Kuliah Diampu'
    )

    cpl_ids = fields.Many2many(
        comodel_name='obe.cpl',
        relation='obe_dosen_cpl_rel',
        column1='dosen_id',
        column2='cpl_id',
        string='CPL Diampu'
    )

    def name_get(self):
        return [(rec.id, f"{rec.name} ({rec.nidn})") for rec in self]
