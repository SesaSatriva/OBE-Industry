from odoo import models, fields
class NilaiCpl(models.Model):
    _name = 'obe.nilai.cpl'
    _description = 'Nilai CPL Mahasiswa'
    _auto = False

    mahasiswa_id = fields.Many2one('obe.mahasiswa')
    cpl_id = fields.Many2one('obe.cpl')
    semester_id = fields.Many2one('obe.semester')

    nilai = fields.Float()
    status = fields.Selection(
        [('tercapai', 'Tercapai'), ('belum', 'Belum')]
    )
