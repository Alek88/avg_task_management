from odoo import models, fields


class TmProject(models.Model):
    """Description of project fields
    The project is one of the main fields of tasks
    """
    _name = 'sg.tm.project'
    _description = 'Project'
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    task_ids = fields.One2many(comodel_name='sg.tm.task',
                               inverse_name='project_id',
                               readonly=True)
    partner_id = fields.Many2one(comodel_name='res.partner')
