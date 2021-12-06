# -*- coding: utf-8 -*-
{
    'name': "sf_res_partner",

    'summary': """
        Only for res.partner model customization""",

    'description': """
        Only for res.partner model customization
    """,

    'author': "Solutionfounder",
    'website': "https://solutionfounder.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/res_partner_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
