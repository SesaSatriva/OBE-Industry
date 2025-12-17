from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PengampuMataKuliah(models.Model):
    _name = 'obe.pengampu.mk'
    _description = 'Pengampu Mata Kuliah'
    _rec_name = 'display_name'

    _sql_constraints = [
        (
            'pengampu_unique',
            'unique(mata_kuliah_id, kelas, semester, tahun_akademik)',
            'Pengampu MK untuk kelas dan semester ini sudah ada'
        )
    ]

    # IDENTITAS AKADEMIK
    mata_kuliah_id = fields.Many2one(
        'obe.mata.kuliah',
        string='Mata Kuliah',
        required=True,
        ondelete='restrict'
    )

    dosen_id = fields.Many2one(
        'obe.dosen',
        string='Dosen Pengampu',
        required=True,
        ondelete='restrict'
    )

    kelas = fields.Char(
        string='Kelas',
        required=True
    )

    semester = fields.Selection(
        [('ganjil', 'Ganjil'), ('genap', 'Genap')],
        string='Semester',
        required=True
    )

    tahun_akademik = fields.Char(
        string='Tahun Akademik',
        required=True
    )

    aktif = fields.Boolean(
        default=True
    )

    # CPMK YANG DIGUNAKAN DI KELAS INI
    cpmk_kelas_ids = fields.One2many(
        'obe.cpmk.kelas',
        'pengampu_id',
        string='CPMK Kelas'
    )

    # KOMPONEN PENILAIAN DI KELAS INI
    komponen_penilaian_ids = fields.One2many(
        'obe.komponen.penilaian',
        'pengampu_id',
        string='Komponen Penilaian'
    )

    display_name = fields.Char(
        compute='_compute_display_name',
        store=True
    )

    @api.depends('mata_kuliah_id', 'kelas', 'semester', 'tahun_akademik')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.mata_kuliah_id.kode} | "
                f"Kelas {rec.kelas} | "
                f"{rec.semester} {rec.tahun_akademik}"
            )

    # VALIDASI BOBOT CPMK = 100%
    @api.constrains('cpmk_kelas_ids')
    def _check_bobot_cpmk(self):
        for rec in self:
            total = sum(rec.cpmk_kelas_ids.mapped('bobot'))
            if total and round(total, 2) != 100.0:
                raise ValidationError('Total bobot CPMK harus 100%')

    # VALIDASI BOBOT KOMPONEN = 100%
    @api.constrains('komponen_penilaian_ids')
    def _check_bobot_komponen(self):
        for rec in self:
            total = sum(rec.komponen_penilaian_ids.mapped('bobot'))
            if total and round(total, 2) != 100.0:
                raise ValidationError('Total bobot komponen penilaian harus 100%')
