from odoo import models, fields


class TmChangeResEmployeeWizard(models.TransientModel):
    """group change of responsible
    """
    _name = 'change.res.employee.wizard'
    _description = 'Сhange of responsible employee'
    responsible_id = fields.Many2one(comodel_name='sg.tm.employee')
    task_ids = fields.Many2many(comodel_name='sg.tm.task')

    def action_adding_res_employee(self):
        for task_id in self.task_ids:
            task_id.responsible_id = self.responsible_id.id
        return {}
