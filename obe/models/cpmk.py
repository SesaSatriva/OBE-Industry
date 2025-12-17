from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Cpmk(models.Model):
    _name = 'obe.cpmk'
    _description = 'Capaian Pembelajaran Mata Kuliah'
    _rec_name = 'display_name'

    _sql_constraints = [
        ('code_unique', 'unique(code, mata_kuliah_id)', 
         'Kode CPMK harus unik dalam satu mata kuliah!')
    ]

    code = fields.Char(
        string='Kode CPMK',
        required=True
    )

    description = fields.Text(
        string='Deskripsi CPMK',
        required=True
    )

    mata_kuliah_id = fields.Many2one(
        'obe.mata.kuliah',
        string='Mata Kuliah',
        required=True,
        ondelete='cascade'
    )

    dosen_pengampu_id = fields.Many2one(
        'obe.dosen',
        string='Dosen Pengampu',
        related='mata_kuliah_id.dosen_pengampu_id',
        store=True,
        readonly=True
    )

    # relasi ke CPL lewat tabel kontribusi
    cpl_line_ids = fields.One2many(
        'obe.cpmk.cpl',
        'cpmk_id',
        string='Kontribusi ke CPL'
    )

    total_bobot_cpl = fields.Float(
        string='Total Bobot ke CPL (%)',
        compute='_compute_total_bobot_cpl',
        store=True
    )

    # relasi ke komponen penilaian (many2many)
    komponen_ids = fields.Many2many(
        'obe.komponen.penilaian',
        'obe_komponen_cpmk_rel',
        'cpmk_id',
        'komponen_id',
        string='Komponen Penilaian'
    )

    display_name = fields.Char(
        compute='_compute_display_name',
        store=True
    )

    @api.depends('code', 'mata_kuliah_id.kode')
    def _compute_display_name(self):
        for rec in self:
            if rec.mata_kuliah_id:
                rec.display_name = f"{rec.code} ({rec.mata_kuliah_id.kode})"
            else:
                rec.display_name = rec.code

    @api.depends('cpl_line_ids.bobot')
    def _compute_total_bobot_cpl(self):
        for rec in self:
            rec.total_bobot_cpl = sum(rec.cpl_line_ids.mapped('bobot'))

    @api.constrains('cpl_line_ids')
    def _check_total_bobot_cpl(self):
        for rec in self:
            if rec.total_bobot_cpl > 100.0 + 1e-6:
                raise ValidationError(
                    f'Total bobot kontribusi CPL untuk {rec.code} melebihi 100%.'
                )
