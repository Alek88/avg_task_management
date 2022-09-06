from odoo import models, fields, _


class TmTaskHistory(models.Model):
    """The object is used to keep a history of tasks.
    This model accumulates key changes in tasks
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
    record_time = fields.Datetime()
    status = fields.Selection([('new', _('New')),
                               ('in_work', _('In work')),
                               ('testing', _('Testing')),
                               ('done', _('Done'))],)
    comment = fields.Char(size=100)
