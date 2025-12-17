from odoo import models, fields

class ProgramStudi(models.Model):
    _name = 'program.studi'
    _description = 'Program Studi'

    name = fields.Char(string='Nama Program Studi', required=True)
    description = fields.Text(string='Deskripsi Singkat')
    vision = fields.Text(string='Visi')
    mission = fields.Text(string='Misi')
    accreditation = fields.Char(string='Akreditasi')
    accreditation_expired = fields.Date(string='Masa Berlaku Akreditasi')
    degree = fields.Char(string='Gelar Lulusan')
    contact_email = fields.Char(string='Email')
    contact_phone = fields.Char(string='Telepon')
    is_published = fields.Boolean(default=True)
