from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CpmkKelasCpl(models.Model):
    _name = 'obe.cpmk.kelas.cpl'
    _description = 'Kontribusi CPMK Kelas terhadap CPL'
    _rec_name = 'cpl_id'

    cpmk_kelas_id = fields.Many2one(
        'obe.cpmk.kelas',
        string='CPMK Kelas',
        required=True,
        ondelete='cascade'
    )

    cpl_id = fields.Many2one(
        'obe.cpl',
        string='CPL',
        required=True,
        ondelete='restrict'
    )

    bobot = fields.Float(
        string='Bobot Kontribusi (%)',
        required=True
    )

    _sql_constraints = [
        (
            'unique_cpmk_kelas_cpl',
            'unique(cpmk_kelas_id, cpl_id)',
            'CPMK Kelas tidak boleh dipetakan dua kali ke CPL yang sama.'
        )
    ]

    @api.constrains('bobot', 'cpmk_kelas_id')
    def _check_total_bobot(self):
        for rec in self:
            if not rec.cpmk_kelas_id:
                continue

            records = self.search([
                ('cpmk_kelas_id', '=', rec.cpmk_kelas_id.id)
            ])

            total = sum(records.mapped('bobot'))

            if round(total, 2) > 100.0:
                raise ValidationError(
                    'Total bobot kontribusi CPL untuk satu CPMK Kelas '
                    'tidak boleh melebihi 100%.'
                )
