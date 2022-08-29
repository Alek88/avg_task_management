from odoo import models, fields


class TmTaskHistory(models.Model):
    """The object is used to keep a history of tasks
    """
    _name = 'sg.tm.task.history'
    _description = 'Task history'
    active = fields.Boolean(default=True)
    name = fields.Char(readonly=True)
    task_id = fields.Many2one(comodel_name='sg.tm.task')
    partner_id = fields.Many2one(comodel_name='res.partner',
                                 readonly=True)
    number_of_minut = fields.Integer(string='Duration')
    responsible_id = fields.Many2one(comodel_name='sg.tm.employee')
    record_date = fields.Date()
