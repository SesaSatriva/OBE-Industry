{
    "name": "OBE Management",
    "version": "1.0.0",
    "summary": "Outcome Based Education Management System",
    "description": "Berisi penilaian OBE yang beracu pada CPL CPMK",
    "category": "Education/OBE",
    "author": "Teknik Industri UNY",
    "website": "https://example.com",
    "license": "LGPL-3",
    "depends": ["base", "web", "website", "portal"],
    "data": [
        "security/obe_group.xml",
        "security/ir.model.access.csv",

        "views/obe_action.xml",
        
        "views/obe_menu.xml",
        
        "views/website_homepage.xml",
        "views/prodi_profil_template.xml",
        "views/program_studi_views.xml",
        "views/page_cpl_public.xml",

        "views/portal_menu.xml",
        
        "views/mahasiswa_views.xml",
        "views/dosen_views.xml",
        "views/mataKuliah_views.xml",
        "views/cpl_views.xml",
        "views/cpmk_views.xml",
        "views/nilai_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            
            # "obe/static/src/xml/cpl_chart.xml",
            "obe/static/src/js/portal_dashboard.js",
            # "obe/static/src/js/cpl_chart.js",
            "obe/static/src/css/portal_dashboard.css",
            "obe/static/src/css/obe_public.css",
        ],
    },
    "installable": True,
    "application": True,
}
