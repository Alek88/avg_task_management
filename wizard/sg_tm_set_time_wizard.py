from odoo import models, fields


class TmSetTimeWizard(models.TransientModel):
    """Adding time for tasks
    """
    _name = 'set.time.wizard'
    _description = 'Set time'
    duration = fields.Integer()
    task_id = fields.Many2one(comodel_name='sg.tm.task',
                              readonly=True)
    employee_id = fields.Many2one(comodel_name='sg.tm.employee',
                                  readonly=True)
    comment = fields.Char(size=100)

    def action_set_time(self):
        self.ensure_one()
        if self.duration != 0:
            self.task_id.write({
                'comment': self.comment,
                'number_of_minut': self.duration,
            })
            #self.task_id.comment = self.comment
            #self.task_id.number_of_minut = self.duration

