from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Mahasiswa(models.Model):
    _name = 'obe.mahasiswa'
    _description = 'Mahasiswa'
    _rec_name = 'display_name'

    _sql_constraints = [
        ('nim_unique', 'unique(nim)', 'NIM harus unik!')
    ]

    name = fields.Char(string='Nama', required=True)
    nim = fields.Char(string='NIM', required=True)
    kelas = fields.Char(string='Kelas')
    rombel = fields.Char(string='Rombel')
    angkatan = fields.Integer(string='Angkatan')

    email = fields.Char(
        string='Email',
        required=True,
        index=True
    )

    user_id = fields.Many2one(
        'res.users',
        string='User Login',
        ondelete='restrict',
        index=True
    )

    # INPUT password (tidak disimpan di DB)
    password = fields.Char(
        string='Password Awal',
        help='Password awal untuk akun portal mahasiswa'
    )

    dosen_pa_id = fields.Many2one(
        'obe.dosen',
        string='Dosen PA'
    )

    mata_kuliah_ids = fields.Many2many(
        'obe.mata.kuliah',
        relation='obe_mahasiswa_mata_kuliah_rel',
        column1='mahasiswa_id',
        column2='mata_kuliah_id',
        string='Mata Kuliah'
    )

    nilai_ids = fields.One2many(
        'obe.nilai',
        'mahasiswa_id',
        string='Nilai'
    )

    display_name = fields.Char(
        compute='_compute_display_name',
        store=True
    )

    @api.depends('name', 'nim')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.nim})"

    @api.model
    def create(self, vals):
        password = vals.pop('password', None)
        rec = super().create(vals)

        if not rec.user_id:
            # cari user berdasarkan email
            user = self.env['res.users'].sudo().search(
                [('login', '=', rec.email)],
                limit=1
            )

            if not user:
                portal_group = self.env.ref('base.group_portal')
                user_vals = {
                    'name': rec.name,
                    'login': rec.email,
                    'email': rec.email,
                    'groups_id': [(6, 0, [portal_group.id])],
                }

                if password:
                    user_vals['password'] = password

                user = self.env['res.users'].sudo().create(user_vals)

            rec.user_id = user.id

        return rec

    def write(self, vals):
        password = vals.pop('password', None)
        res = super().write(vals)

        if password:
            for rec in self:
                if rec.user_id:
                    rec.user_id.sudo().write({
                        'password': password
                    })
        return res
