from odoo import models, fields
import datetime

class TmEmployeeReportWizard(models.TransientModel):
    """
    """
    _name = 'settings.emp.report.wizard'
    _description = 'Settings employee report wizard'
    employee_ids = fields.Many2many(comodel_name='sg.tm.employee',
                                  readonly=True)
    start_time = fields.Datetime(default=datetime.datetime.now(),
                             required=True)
    end_time = fields.Datetime(default=datetime.datetime.now(),
                           required=True)
    
    def action_show_report(self):
        employee_ids = self.env['sg.tm.employee'].search_read([('id', 'in', self.employee_ids.ids)])  
        data = {
            'form': self.read()[0],
            'employee_ids': employee_ids,
        }
        return self.env.ref('sg_task_management.action_report_employee').report_action(self, data=data)
    