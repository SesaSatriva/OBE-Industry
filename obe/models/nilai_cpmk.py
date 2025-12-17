from odoo import models, fields, api

class NilaiCpmk(models.Model):
    _name = 'obe.nilai.cpmk'
    _description = 'Nilai CPMK Mahasiswa'

    mahasiswa_id = fields.Many2one('obe.mahasiswa', required=True)
    cpmk_id = fields.Many2one('obe.cpmk', required=True)
    mata_kuliah_id = fields.Many2one('obe.mata.kuliah', required=True)
    semester = fields.Char(required=True)

    nilai = fields.Float(
        compute='_compute_nilai',
        store=True
    )

    @api.depends(
        'mahasiswa_id',
        'cpmk_id',
        'semester'
    )
    def _compute_nilai(self):
        for rec in self:
            nilai_komponen = self.env['obe.nilai.komponen'].search([
                ('mahasiswa_id', '=', rec.mahasiswa_id.id),
                ('cpmk_id', '=', rec.cpmk_id.id),
                ('semester', '=', rec.semester),
            ])

            total = 0.0
            for nk in nilai_komponen:
                total += (nk.bobot / 100.0) * nk.nilai

            rec.nilai = total
class NilaiMk(models.Model):
    _name = 'obe.nilai.mk'
    _description = 'Nilai Mata Kuliah Mahasiswa'

    mahasiswa_id = fields.Many2one('obe.mahasiswa', required=True)
    mata_kuliah_id = fields.Many2one('obe.mata.kuliah', required=True)
    semester = fields.Char(required=True)

    nilai = fields.Float(
        compute='_compute_nilai',
        store=True
    )

    @api.depends('mahasiswa_id', 'mata_kuliah_id', 'semester')
    def _compute_nilai(self):
        for rec in self:
            nilai_cpmk = self.env['obe.nilai.cpmk'].search([
                ('mahasiswa_id', '=', rec.mahasiswa_id.id),
                ('mata_kuliah_id', '=', rec.mata_kuliah_id.id),
                ('semester', '=', rec.semester),
            ])

            total = 0.0
            for nc in nilai_cpmk:
                total += (nc.cpmk_id.bobot / 100.0) * nc.nilai

            rec.nilai = total

