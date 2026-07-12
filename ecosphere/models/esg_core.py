from odoo import models, fields, api

class EsgCategory(models.Model):
    _name = 'ecosphere.category'
    _description = 'ESG Category'

    name = fields.Char(string='Name', required=True)
    category_type = fields.Selection([
        ('csr', 'CSR Activity'),
        ('challenge', 'Challenge')
    ], string='Type', required=True)
    active = fields.Boolean(default=True, string='Status')

class EsgEmissionFactor(models.Model):
    _name = 'ecosphere.emission.factor'
    _description = 'Emission Factor'

    name = fields.Char(string='Name', required=True)
    carbon_value_per_unit = fields.Float(string='Carbon Value (kg CO2e)', required=True, help="Emissions generated per unit")
    uom = fields.Char(string='Unit of Measure (e.g., L, kg, kWh)')
    active = fields.Boolean(default=True)

class EsgCarbonTransaction(models.Model):
    _name = 'ecosphere.carbon.transaction'
    _description = 'Carbon Transaction'

    name = fields.Char(string='Reference/Source', required=True, help="e.g., PO-00124 or Fleet Fuel Log")
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    emission_factor_id = fields.Many2one('ecosphere.emission.factor', string='Emission Factor', required=True)
    quantity = fields.Float(string='Quantity Used', required=True)
    
    # The magical auto-calculating field requested in the MVP scope
    calculated_emissions = fields.Float(
        string='Calculated Emissions (kg CO2e)', 
        compute='_compute_emissions', 
        store=True
    )
    date = fields.Date(string='Date', default=fields.Date.context_today)

    @api.depends('emission_factor_id', 'quantity')
    def _compute_emissions(self):
        for record in self:
            record.calculated_emissions = record.quantity * record.emission_factor_id.carbon_value_per_unit