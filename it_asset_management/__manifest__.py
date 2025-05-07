# -*- coding: utf-8 -*-
{
    'name': "Gestionnaire de parc informatique",

    'summary': 'Module pour gérer le parc informatique et la facturation récurrente',
    'description': """
        Module Odoo pour la gestion de parc informatique multi-client avec facturation récurrente,
        suivi des incidents et alertes automatiques.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'helpdesk', 'stock', 'account', 'hr', 'mail','portal','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/asset.xml',
        'views/portal_templates.xml',
        'views/contract_views.xml',
        'views/incident_view.xml',
        'views/parc_views.xml',
        'views/maintenance_views.xml',
        'views/equipment_views.xml',
        'data/maintenance_cron.xml',
        'views/templates.xml',
        'views/client_views.xml',
        'views/intervention_views.xml',
        'views/menu_views.xml',
        'data/cron.xml',
    ],
    'py_files': [
        'controllers/portal.py',
    ],
    'assets': {
        'web.assets_frontend': [
            '/it_asset_management/static/src/scss/portal.scss',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,

}

