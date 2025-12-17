from odoo import models, fields

class MataKuliah(models.Model):
    _name = 'obe.mata.kuliah'
    _description = 'Mata Kuliah'

    _sql_constraints = [
        ('matakuliah_ids_unique', 'unique(matakuliah_ids)', 'Kode Mata Kuliah harus unik!')
    ]

    matakuliah_ids = fields.Char(string='Kode Mata Kuliah', required=True)
    name = fields.Char(string='Nama Mata Kuliah', required=True)
    sks = fields.Integer(string='SKS', required=True)

    tipe = fields.Selection(
        selection=[
            ('teori', 'Teori'),
            ('praktikum', 'Praktikum')
        ],
        string='Tipe Mata Kuliah',
        required=True
    )

    mahasiswa_id = fields.Many2many(
        comodel_name='obe.mahasiswa',
        relation='obe_mahasiswa_mata_kuliah_rel',
        column1='mata_kuliah_id',
        column2='mahasiswa_id',
        string='Mahasiswa'
    )


    dosen_ids = fields.Many2many(
        comodel_name='obe.dosen',
        relation='obe_mk_dosen_rel',
        column1='mata_kuliah_id',
        column2='dosen_id',
        string='Dosen Pengampu'
    )

    cpl_ids = fields.Many2many(
        'obe.cpl',
        'obe_mata_kuliah_cpl_rel',
        'mata_kuliah_id',
        'cpl_id',
        string='CPL Mapping'
    )