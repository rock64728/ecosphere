from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CsrActivity(models.Model):
    _name = 'ecosphere.csr.activity'
    _description = 'CSR Activity'

    name = fields.Char(string='Title', required=True)
    # This domain ensures only CSR categories show up in the dropdown
    category_id = fields.Many2one('ecosphere.category', string='Category', domain=[('category_type', '=', 'csr')])
    description = fields.Text(string='Description')
    points_offered = fields.Integer(string='Points Offered', required=True, default=10)
    date = fields.Date(string='Date')
    active = fields.Boolean(default=True)

class EmployeeParticipation(models.Model):
    _name = 'ecosphere.participation'
    _description = 'Employee CSR Participation'

    activity_id = fields.Many2one('ecosphere.csr.activity', string='CSR Activity', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    proof = fields.Binary(string='Proof of Participation', attachment=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Approval Status', default='draft')
    
    completion_date = fields.Date(string='Completion Date', default=fields.Date.context_today)
    points_earned = fields.Integer(string='Points Earned', compute='_compute_points', store=True)

    # Auto-calculate points only when approved
    @api.depends('state', 'activity_id.points_offered')
    def _compute_points(self):
        for record in self:
            if record.state == 'approved':
                record.points_earned = record.activity_id.points_offered
            else:
                record.points_earned = 0

    # MVP Business Rule: Evidence Requirement validation
    def action_approve(self):
        for record in self:
            if not record.proof:
                raise ValidationError("Hackathon Rule: Proof of participation is required before approval!")
            record.state = 'approved'

    def action_reject(self):
        for record in self:
            record.state = 'rejected'