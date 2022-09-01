from odoo import models, fields


class TmEmployee(models.Model):
    """Description of employee fields
    """
    _name = 'sg.tm.employee'
    _description = 'Employee'
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    user_id = fields.Many2one(comodel_name='res.users',
                              default=lambda self: self.env.user.id)
    task_ids = fields.One2many(comodel_name='sg.tm.task',
                               inverse_name='responsible_id',
                               readonly=True)
    task_history_ids = fields.One2many(comodel_name='sg.tm.task.history',
                               inverse_name='responsible_id',
                               readonly=True)
