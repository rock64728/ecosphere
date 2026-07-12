from odoo import models, fields, api

class DepartmentScore(models.Model):
    _name = 'ecosphere.department.score'
    _description = 'Department ESG Score'
    _rec_name = 'department_id'

    department_id = fields.Many2one('hr.department', string='Department', required=True)
    env_score = fields.Float(string='Environmental Score', compute='_compute_scores', store=True)
    soc_score = fields.Float(string='Social Score', compute='_compute_scores', store=True)
    gov_score = fields.Float(string='Governance Score', default=85.0, help="Defaulted for MVP") 
    total_score = fields.Float(string='Total ESG Score', compute='_compute_scores', store=True)

    @api.depends('department_id')
    def _compute_scores(self):
        for record in self:
            if not record.department_id:
                record.env_score = 0
                record.soc_score = 0
                record.total_score = 0
                continue

            # 1. Environmental: Calculate based on Carbon Transactions
            emissions = self.env['ecosphere.carbon.transaction'].search([
                ('department_id', '=', record.department_id.id)
            ])
            total_emissions = sum(emissions.mapped('calculated_emissions'))
            # MVP Logic: Start at 100, lose points for high emissions
            calc_env = max(0.0, 100.0 - (total_emissions / 100.0))
            
            # 2. Social: Calculate based on Employee CSR Points in this department
            participations = self.env['ecosphere.participation'].search([
                ('employee_id.department_id', '=', record.department_id.id),
                ('state', '=', 'approved')
            ])
            total_points = sum(participations.mapped('points_earned'))
            # MVP Logic: Start at 50 base points, add points for CSR participation
            calc_soc = min(100.0, 50.0 + (total_points / 5.0))
            
            record.env_score = calc_env
            record.soc_score = calc_soc
            
            # 3. Governance: Hardcoded to 85.0 for MVP time constraints
            
            # THE HACKATHON RULE: 40% Env, 30% Soc, 30% Gov
            record.total_score = (calc_env * 0.40) + (calc_soc * 0.30) + (record.gov_score * 0.30)