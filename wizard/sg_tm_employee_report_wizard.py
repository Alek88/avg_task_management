import datetime
from odoo import models, fields


class TmEmployeeReportWizard(models.TransientModel):
    """Wizard for setting up a report on worked minutes.
    Called from the work tree.
    """
    _name = 'settings.emp.report.wizard'
    _description = 'Settings employee report wizard'
    employee_ids = fields.Many2many(comodel_name='sg.tm.employee',
                                    readonly=True)
    start_time = fields.Datetime(
        default=datetime.datetime.now().replace(hour=0, minute=0, second=0),
        required=True)
    end_time = fields.Datetime(
        default=datetime.datetime.now().replace(hour=23, minute=59, second=59),
        required=True)

    def action_show_report(self):
        """The method collects all the necessary information for the report.
        Returns:
            action_report_employee: Returns data for the report
        """
        employee_ids = self.env['sg.tm.employee'].search_read([
            ('id', 'in', self.employee_ids.ids)])
        for employee_id in employee_ids:
            work_time = 0
            task_history_ids = self.env['sg.tm.task.history'].search_read([
                ('responsible_id', '=', employee_id.get('id')),
                ('record_time', '>=', self.start_time),
                ('record_time', '<', self.end_time)])
            for task_id in task_history_ids:
                tasks = self.env['sg.tm.task'].search([
                    ('id', '=', task_id.get('task_id')[0])])
                task_id['project_name'] = tasks.project_id.name
                task_id['task_name'] = tasks.name
                work_time += task_id.get('number_of_minut')
            employee_id['task_hist_ids'] = task_history_ids
            employee_id['work_time'] = work_time
        data = {
            'form': self.read()[0],
            'employee_ids': employee_ids,
        }
        return self.env.ref('sg_task_management.action_report_employee').\
            report_action(self, data=data)
