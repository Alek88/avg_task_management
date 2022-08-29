from odoo import models, fields


class TmPrice(models.Model):
    """designed to estimate the cost of work performed
    """
    _name = 'sg.tm.price'
    _description = 'Price'
    active = fields.Boolean(default=True)
    name = fields.Char()
    partner_id = fields.Many2one(comodel_name='res.partner',
                                 required=True)
    price = fields.Monetary(currency_field='currency_id')
    employee_id = fields.Many2one(comodel_name='sg.tm.employee',
                                  required=True)
    currency_id = fields.Many2one(comodel_name='res.currency',
                                  string='Currency',
                                  store=True,
                                  readonly=False,
                                  help="The payment's currency.")
