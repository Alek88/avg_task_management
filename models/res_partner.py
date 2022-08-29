from odoo import models, fields


class TmResPartner(models.Model):
    """extends the res.partner model
    and adds the task_ids field
    """
    _inherit = ['res.partner']
    task_ids = fields.One2many(comodel_name='sg.tm.task',
                               inverse_name='partner_id')
