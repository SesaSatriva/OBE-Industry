from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NilaiKomponen(models.Model):
    _name = 'obe.nilai.komponen'
    _description = 'Nilai Komponen Mahasiswa'
    _rec_name = 'display_name'

    mahasiswa_id = fields.Many2one(
        'obe.mahasiswa',
        string='Mahasiswa',
        required=True,
        ondelete='cascade'
    )

    komponen_id = fields.Many2one(
        'obe.komponen.penilaian',
        string='Komponen Penilaian',
        required=True,
        ondelete='cascade'
    )

    pengampu_id = fields.Many2one(
        related='komponen_id.pengampu_id',
        store=True,
        readonly=True
    )

    nilai = fields.Float(
        string='Nilai',
        required=True
    )

    display_name = fields.Char(
        compute='_compute_display_name',
        store=True
    )

    _sql_constraints = [
        (
            'unique_nilai_mahasiswa_komponen',
            'unique(mahasiswa_id, komponen_id)',
            'Mahasiswa sudah memiliki nilai untuk komponen ini.'
        )
    ]

    @api.depends('mahasiswa_id', 'komponen_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.mahasiswa_id.display_name} - "
                f"{rec.komponen_id.kode}"
            )

    @api.constrains('nilai')
    def _check_nilai_range(self):
        for rec in self:
            if rec.nilai < 0 or rec.nilai > 100:
                raise ValidationError('Nilai harus berada pada rentang 0–100.')