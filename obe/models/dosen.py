from odoo import models, fields


class Dosen(models.Model):
    _name = 'obe.dosen'
    _description = 'Dosen'
    _rec_name = 'display_name'

    _sql_constraints = [
        ('nidn_unique', 'unique(nidn)', 'NIDN harus unik!')
    ]

    name = fields.Char(
        string='Nama',
        required=True
    )

    nidn = fields.Char(
        string='NIDN',
        required=True
    )

    email = fields.Char(
        string='Email',
        index=True
    )

    # DOSEN PEMBIMBING AKADEMIK
    mahasiswa_ids = fields.One2many(
        'obe.mahasiswa',
        'dosen_pa_id',
        string='Mahasiswa Bimbingan'
    )

    display_name = fields.Char(
        compute='_compute_display_name',
        store=True
    )

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.nidn})"

    def name_get(self):
        return [(rec.id, rec.display_name) for rec in self]
