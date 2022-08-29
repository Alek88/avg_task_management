from odoo import models, fields


class TmSetTimeWizard(models.TransientModel):
    """Adding time for tasks
    """
    _name = 'set.time.wizard'
    _description = 'Set time'
    duration = fields.Integer()
    task_id = fields.Many2one(comodel_name='sg.tm.task',
                              readonly=True)

    def action_set_time(self):
        self.ensure_one()
        val = self.env['sg.tm.task.history'].search([
            ('task_id', '=', self.task_id.id),
            ('responsible_id', '=', self.task_id.responsible_id.id)])
        if val:
            val.number_of_minut += self.duration
        self.task_id.number_of_minut += self.duration
        return {}
