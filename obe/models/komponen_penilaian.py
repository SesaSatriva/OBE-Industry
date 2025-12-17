from odoo import models, fields, api
from odoo.exceptions import ValidationError


class KomponenPenilaian(models.Model):
    _name = 'obe.komponen.penilaian'
    _description = 'Komponen Penilaian'
    _rec_name = 'kode'

    JENIS_KOMPONEN = [
        ('tugas', 'Tugas'),
        ('kuis', 'Kuis'),
        ('uts', 'UTS'),
        ('uas', 'UAS'),
        ('praktikum', 'Praktikum'),
        ('proyek', 'Proyek'),
        ('presentasi', 'Presentasi'),
        ('lainnya', 'Lainnya'),
    ]

    PREFIX_MAP = {
        'tugas': 'TGS',
        'kuis': 'KUIS',
        'uts': 'UTS',
        'uas': 'UAS',
        'praktikum': 'PRK',
        'proyek': 'PRJ',
        'presentasi': 'PRS',
        'lainnya': 'OTH',
    }

    pengampu_id = fields.Many2one(
        'obe.pengampu.mk',
        required=True,
        ondelete='cascade'
    )

    jenis = fields.Selection(
        JENIS_KOMPONEN,
        required=True
    )

    kode = fields.Char(
        readonly=True,
        copy=False
    )

    bobot = fields.Float(
        string='Bobot terhadap MK (%)',
        required=True
    )

    keterangan = fields.Char()

    cpmk_rel_ids = fields.One2many(
        'obe.komponen.cpmk',
        'komponen_id',
        string='Distribusi CPMK'
    )

    _sql_constraints = [
        (
            'unique_kode_pengampu',
            'unique(kode, pengampu_id)',
            'Kode komponen harus unik dalam satu kelas.'
        )
    ]

    @api.model
    def create(self, vals):
        if not vals.get('kode') and vals.get('jenis') and vals.get('pengampu_id'):
            prefix = self.PREFIX_MAP.get(vals['jenis'])
            existing = self.search([
                ('pengampu_id', '=', vals['pengampu_id']),
                ('kode', 'like', f'{prefix}%')
            ])

            nums = []
            for r in existing:
                s = r.kode.replace(prefix, '')
                if s.isdigit():
                    nums.append(int(s))

            next_num = max(nums) + 1 if nums else 1
            vals['kode'] = f'{prefix}{next_num}'

        return super().create(vals)

    @api.constrains('cpmk_rel_ids')
    def _check_cpmk_distribution(self):
        for rec in self:
            total = sum(rec.cpmk_rel_ids.mapped('bobot'))
            if rec.cpmk_rel_ids and round(total, 2) != 100.0:
                raise ValidationError(
                    'Total bobot distribusi CPMK pada satu komponen harus 100%.'
                )
