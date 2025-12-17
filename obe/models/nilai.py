from odoo import models, fields, api
class Nilai(models.Model):
    _name = 'obe.nilai'
    _description = 'Nilai Mahasiswa'

    _sql_constraints = [
        (
            'unique_mahasiswa_mk',
            'unique(mahasiswa_id, mata_kuliah_id)',
            'Satu mahasiswa hanya boleh punya satu nilai per mata kuliah!'
        )
    ]

    mahasiswa_id = fields.Many2one(
        'obe.mahasiswa', string='Mahasiswa', required=True, ondelete='cascade'
    )
    mata_kuliah_id = fields.Many2one(
        'obe.mata.kuliah', string='Mata Kuliah', required=True
    )

    nilai_angka = fields.Float(string='Nilai Angka', required=True)
    nilai_huruf = fields.Char(
        string='Nilai Huruf',
        compute='_compute_nilai_huruf',
        store=True
    )

    @api.depends('nilai_angka')
    def _compute_nilai_huruf(self):
        for rec in self:
            rec.nilai_huruf = (
                'A' if rec.nilai_angka >= 85 else
                'B' if rec.nilai_angka >= 70 else
                'C' if rec.nilai_angka >= 55 else
                'D' if rec.nilai_angka >= 40 else
                'E'
            )
