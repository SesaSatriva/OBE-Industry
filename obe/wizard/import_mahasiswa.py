from odoo import models, fields, _
from odoo.exceptions import UserError
import base64
import csv
import io

try:
    import xlrd
except ImportError:
    xlrd = None


class ImportMahasiswaWizard(models.TransientModel):
    _name = "import.mahasiswa.wizard"
    _description = "Import Mahasiswa (CSV / Excel)"

    file_data = fields.Binary(string="File", required=True)
    file_name = fields.Char(string="Nama File")

    def action_import(self):
        if not self.file_data:
            raise UserError(_("Silakan pilih file terlebih dahulu."))

        data = base64.b64decode(self.file_data)
        filename = (self.file_name or "").lower()

        if filename.endswith(".csv"):
            self._import_csv(data)
        elif filename.endswith((".xls", ".xlsx")):
            if not xlrd:
                raise UserError(_("Library xlrd tidak tersedia."))
            self._import_xls(data)
        else:
            raise UserError(_("Format file tidak dikenali. Gunakan CSV atau Excel."))

        return {"type": "ir.actions.client", "tag": "reload"}

    def _normalize_headers(self, headers):
        return [str(h).strip().lower().replace(" ", "_") for h in headers]

    # ================= CSV =================
    def _import_csv(self, data):
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = data.decode("latin-1")

        reader = csv.DictReader(io.StringIO(text))
        reader.fieldnames = self._normalize_headers(reader.fieldnames or [])

        for row in reader:
            clean_row = {
                k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()
            }
            self._create_or_update_mahasiswa(clean_row)

    # ================= EXCEL =================
    def _import_xls(self, data):
        workbook = xlrd.open_workbook(file_contents=data)
        sheet = workbook.sheet_by_index(0)

        headers = self._normalize_headers(
            [sheet.cell_value(0, col) for col in range(sheet.ncols)]
        )

        for row_idx in range(1, sheet.nrows):
            row = {}
            for col_idx, header in enumerate(headers):
                value = sheet.cell_value(row_idx, col_idx)
                if isinstance(value, float) and value.is_integer():
                    value = int(value)
                row[header] = value
            self._create_or_update_mahasiswa(row)

    # ================= CREATE / UPDATE =================
    def _create_or_update_mahasiswa(self, row):
        nim = str(row.get("nim") or "").split(".")[0].strip()
        name = str(row.get("name") or "").strip()
        email = str(row.get("email") or "").strip()
        password = str(row.get("password") or "").strip()

        if not nim or not name:
            return

        dosen_pa_id = False
        dosen_name = str(row.get("dosen_pa") or "").strip()
        if dosen_name:
            dosen = self.env["obe.dosen"].search(
                [("name", "ilike", dosen_name)], limit=1
            )
            dosen_pa_id = dosen.id

        vals = {
            "nim": nim,
            "name": name,
            "kelas": str(row.get("kelas") or "").strip(),
            "rombel": str(row.get("rombel") or "").strip(),
            "angkatan": int(row.get("angkatan"))
            if str(row.get("angkatan") or "").isdigit()
            else False,
            "email": email,
            "dosen_pa_id": dosen_pa_id,
        }

        Mahasiswa = self.env["obe.mahasiswa"].sudo()
        Users = self.env["res.users"].sudo()

        mahasiswa = Mahasiswa.search([("nim", "=", nim)], limit=1)
        if not mahasiswa:
            mahasiswa = Mahasiswa.create(vals)
        else:
            mahasiswa.write(vals)

        # ===== USER HANDLING =====
        user = mahasiswa.user_id

        if not user:
            # cari user berdasarkan login/email
            user = Users.search(
                ["|", ("login", "=", email), ("login", "=", nim)],
                limit=1
            )

        if not user:
            # create user portal
            portal_group = self.env.ref("base.group_portal")
            user_vals = {
                "name": mahasiswa.name,
                "login": email or nim,
                "email": email,
                "groups_id": [(6, 0, [portal_group.id])],
            }
            if password:
                user_vals["password"] = password

            user = Users.create(user_vals)

        else:
            # update password jika diisi
            if password:
                user.write({"password": password})

        if mahasiswa.user_id != user:
            mahasiswa.write({"user_id": user.id})


