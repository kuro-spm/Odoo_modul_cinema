{ 
    'name': 'cinema_maig2025', 
    'version': '1.0', 
    'category': 'Education', 
    'summary': 'Educational module for Odoo practice', 
        '''Module prepared by department 'Informatica i comunicacions' 
        of Institute Mila i Fontanals in Igualada (Barcelona-Spain) 
        for learning in development and adaptation of modules of Odoo ERP. 
 
        It is part of the learning materials for the module 
        'Sistemes de gestio empresarial' in the course 
        'CFS Desenvolupament d'aplicacions multiplataforma.''' 
    'author': 'Sara Prats Morales', 
    'website': 'http://www.infomila.info', 
    'license': 'LGPL-3', 
    'depends': ['base'], 
    'data': [ 
        #'security/ir.model.access.csv', 
        'views/actions.xml', 
        'views/menus.xml', 
    ], 
    'installable': True, 
    'application': True, 
} 
