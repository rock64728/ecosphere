{
    'name': 'EcoSphere ESG Management Platform',
    'version': '1.0',
    'summary': 'Integrate ESG tracking directly into ERP operations',
    'description': """
        EcoSphere ESG Management Platform
        =================================
        Modules included:
        * Environmental: Carbon tracking and emissions
        * Social: CSR activities and employee participation
        * Governance: Compliance tracking and audits
        * Gamification: Challenges, leaderboards, and rewards
    """,
    'category': 'Sustainability',
    'author': 'Jenil Prajapati',
    'depends': ['base', 'hr', 'mail', 'board'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/esg_core_views.xml',
        'views/esg_social_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}