{
    'name': 'cinema_maig2025',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Educational module for Odoo practice',
    'description': '''Module prepared by department Informatica i comunicacions
        of Institute Mila i Fontanals in Igualada (Barcelona-Spain)
        for learning in development and adaptation of modules of Odoo ERP.

        It is part of the learning materials for the module
        Sistemes de gestio empresarial in the course
        CFS Desenvolupament d\'aplicacions multiplataforma.''',
    'author': 'Sara Prats Morales',
    'website': 'http://www.infomila.info',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/menus.xml',
        'views/cinema_film_views.xml',
        'views/cinema_person_views.xml',
        'views/country_info.xml',
        'report/cinema_film_report.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
}
