from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EsgChallenge(models.Model):
    _name = 'ecosphere.challenge'
    _description = 'Sustainability Challenge'

    name = fields.Char(string='Title', required=True)
    # Domain ensures only 'challenge' categories appear
    category_id = fields.Many2one('ecosphere.category', string='Category', domain=[('category_type', '=', 'challenge')])
    description = fields.Text(string='Description')
    xp_reward = fields.Integer(string='XP Reward', required=True, default=50)
    deadline = fields.Date(string='Deadline')
    
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('active', 'Active'), 
        ('archived', 'Archived')
    ], string='Status', default='draft')

class EsgReward(models.Model):
    _name = 'ecosphere.reward'
    _description = 'ESG Reward Catalog'

    name = fields.Char(string='Reward Name', required=True)
    description = fields.Text(string='Description')
    points_required = fields.Integer(string='Points Required', required=True)
    stock_status = fields.Integer(string='Stock Available', required=True, default=10)

class RewardRedemption(models.Model):
    _name = 'ecosphere.reward.redemption'
    _description = 'Reward Redemption Tracking'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    reward_id = fields.Many2one('ecosphere.reward', string='Reward', required=True)
    date = fields.Date(string='Date Redeemed', default=fields.Date.context_today)

    # MVP Business Rule: Stock validation & auto-deduction
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            reward = self.env['ecosphere.reward'].browse(vals.get('reward_id'))
            if reward.stock_status <= 0:
                raise ValidationError("Hackathon Rule: This reward is currently out of stock!")
            # Deduct the stock automatically when a redemption record is created
            reward.stock_status -= 1
        return super().create(vals_list)