from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CpmkCpl(models.Model):
    _name = 'obe.cpmk.cpl'
    _description = 'Kontribusi CPMK terhadap CPL'
    _rec_name = 'cpl_id'

    cpmk_id = fields.Many2one(
        'obe.cpmk',
        string='CPMK',
        required=True,
        ondelete='cascade'
    )

    cpl_id = fields.Many2one(
        'obe.cpl',
        string='CPL',
        required=True,
        ondelete='cascade'
    )

    bobot = fields.Float(
        string='Bobot Kontribusi (%)',
        required=True
    )

    _sql_constraints = [
        (
            'unique_cpmk_cpl',
            'unique(cpmk_id, cpl_id)',
            'CPMK tidak boleh dipetakan dua kali ke CPL yang sama.'
        )
    ]

    @api.constrains('bobot', 'cpmk_id')
    def _check_total_bobot_cpmk(self):
        for rec in self:
            if not rec.cpmk_id:
                continue

            records = self.search([('cpmk_id', '=', rec.cpmk_id.id)])
            total = sum(records.mapped('bobot'))

            if total > 100.0 + 1e-6:
                raise ValidationError(
                    f'Total bobot CPL untuk {rec.cpmk_id.code} melebihi 100%.'
                )
