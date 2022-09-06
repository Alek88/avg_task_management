from odoo import models, fields, api


class TmSetTimeWizard(models.TransientModel):
    """Adding time for tasks
    Called by a button from the kanban for the task model
    """
    _name = 'set.time.wizard'
    _description = 'Set time'
    duration = fields.Integer()
    task_id = fields.Many2one(comodel_name='sg.tm.task',
                              readonly=True)
    employee_id = fields.Many2one(comodel_name='sg.tm.employee',
                                  compute='_compute_employee',
                                  readonly=True)
    comment = fields.Char(size=100)

    @api.depends('task_id')
    def _compute_employee(self):
        if self.task_id:
            self.employee_id = self.task_id.responsible_id

    def action_set_time(self):
        """Changes data for task fields
        """
        self.ensure_one()
        if self.duration != 0:
            self.task_id.write({
                'comment': self.comment,
                'number_of_minut': self.duration,
            })
