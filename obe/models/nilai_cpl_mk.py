from odoo import models, fields

class NilaiCplMk(models.Model):
    _name = 'obe.nilai.cpl.mk'
    _description = 'Nilai CPL Mahasiswa per Mata Kuliah'
    _auto = False

    mahasiswa_id = fields.Many2one('obe.mahasiswa')
    cpl_id = fields.Many2one('obe.cpl')
    mata_kuliah_id = fields.Many2one('obe.mata.kuliah')
    semester_id = fields.Many2one('obe.semester')

    nilai = fields.Float()
