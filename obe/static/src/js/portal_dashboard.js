/** @odoo-module **/

document.addEventListener('DOMContentLoaded', () => {
    // === Highlight baris nilai ===
    const rows = document.querySelectorAll(
        '.o_obe_portal_dashboard table tbody tr'
    );

    rows.forEach((row) => {
        const cell = row.querySelector('[data-nilai]');
        if (!cell) return;

        const nilai = parseFloat(cell.dataset.nilai);
        if (isNaN(nilai)) return;

        row.classList.remove('table-danger', 'table-warning', 'table-success');

        if (nilai < 60) {
            row.classList.add('table-danger');
        } else if (nilai < 80) {
            row.classList.add('table-warning');
        } else {
            row.classList.add('table-success');
        }
    });
});
