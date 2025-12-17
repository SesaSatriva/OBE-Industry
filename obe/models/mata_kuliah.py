from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CplMataKuliah(models.Model):
    _name = 'obe.cpl.mata.kuliah'
    _description = 'Kontribusi Mata Kuliah terhadap CPL'
    _rec_name = 'mata_kuliah_id'

    cpl_id = fields.Many2one(
        'obe.cpl',
        string='CPL',
        required=True,
        ondelete='cascade'
    )

    mata_kuliah_id = fields.Many2one(
        'obe.mata.kuliah',
        string='Mata Kuliah',
        required=True,
        ondelete='cascade'
    )

    bobot = fields.Float(
        string='Bobot Kontribusi (%)',
        required=True
    )

    _sql_constraints = [
        (
            'unique_cpl_mk',
            'unique(cpl_id, mata_kuliah_id)',
            'Mata kuliah tidak boleh didaftarkan dua kali pada CPL yang sama.'
        )
    ]

    @api.constrains('bobot', 'cpl_id')
    def _check_total_bobot_cpl(self):
        for rec in self:
            if not rec.cpl_id:
                continue

            records = self.search([('cpl_id', '=', rec.cpl_id.id)])
            total = sum(records.mapped('bobot'))

            if total > 100.0 + 1e-6:
                raise ValidationError(
                    f'Total bobot mata kuliah untuk {rec.cpl_id.cpl_ids} melebihi 100%.'
                )
