import datetime
from calendar import monthrange
from odoo import models, fields, api


class TmBilling(models.Model):
    """Сalculation of revenue for completed tasks
    """
    _name = 'sg.tm.billing'
    _description = 'Billing'
    active = fields.Boolean(default=True)
    name = fields.Char(compute='_compute_name',
                       store=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    project_id = fields.Many2one(comodel_name='sg.tm.project',
                                 required=True)
    partner_id = fields.Many2one(comodel_name='res.partner',
                                 readonly=True,
                                 compute='_compute_partner')
    currency_id = fields.Many2one(comodel_name='res.currency',
                                  string='Currency',
                                  store=True,
                                  readonly=True,
                                  compute='_compute_get_price',
                                  help="The payment's currency.")
    price = fields.Monetary(currency_field='currency_id',
                            compute='_compute_get_price',
                            store=True)
    summ = fields.Monetary(currency_field='currency_id',
                           compute='_compute_summ')
    employee_id = fields.Many2one(comodel_name='sg.tm.employee',
                                  required=True)
    field_visibility = fields.Boolean(compute='_compute_visibility',
                                      default=True)

    @api.depends('start_date', 'end_date', 'project_id', 'employee_id')
    def _compute_name(self):
        for rec in self:
            if rec.employee_id and rec.project_id\
                    and rec.start_date and rec.end_date:
                rec.name = f"{rec.employee_id.name}, {rec.project_id.name}\
                    ({rec.start_date} - {rec.end_date})"
            else:
                rec.name = ''

    @api.depends('employee_id')
    def _compute_visibility(self, user=None):
        """Hides the price and amount if the user does not
        match the role or for other people's records
        """
        if self.env.user.has_group('sg_task_management.group_tm_admin') or\
            self.env.user.has_group('base.group_system') or\
                self.employee_id.user_id == self.env.user:
            self.field_visibility = False
        else:
            self.field_visibility = True

    @api.depends('project_id', 'employee_id')
    def _compute_get_price(self):
        """The method finds the price by the "project_id"
        and "employee_id fields,
        and also finds the partner and currency.
        :param notify_type: none
        :return None:
        """
        for rec in self:
            price = 0
            currency_id = 0
            if rec.project_id.id:
                if rec.employee_id.id:
                    price_id = self.env['sg.tm.price'].search([
                        ('partner_id', '=', rec.partner_id.id),
                        ('employee_id', '=', rec.employee_id.id)])
                    if price_id:
                        price = price_id.price
                        currency_id = price_id.currency_id.id
            rec.price = price
            rec.currency_id = currency_id

    @api.depends('project_id')
    def _compute_partner(self):
        """The method finds the price by the "project_id"
        and "employee_id fields,
        and also finds the partner and currency.
        :param notify_type: none
        :return None:
        """
        for rec in self:
            if rec.project_id.id:
                rec.partner_id = rec.project_id.partner_id.id
            else:
                rec.partner_id = 0

    @api.depends('project_id', 'employee_id', 'start_date', 'end_date')
    def _compute_summ(self):
        """The method finds all completed tasks for the specified period
        and calculates the total cost.
        :param notify_type: none
        :return None:
        """
        for rec in self:
            all_summ = 0
            if rec.project_id and rec.employee_id and rec.start_date \
                    and rec.end_date:
                task_history_ids = self.env['sg.tm.task.history'].search([
                    ('partner_id', '=', rec.partner_id.id),
                    ('responsible_id', '=', rec.employee_id.id),
                    ('task_id.status', '=', 'done'),
                    ('record_time', '>=', rec.start_date),
                    ('record_time', '<=', rec.end_date)])
                if task_history_ids:
                    minutes = 0
                    for task_history in task_history_ids:
                        minutes += task_history.number_of_minut
                    all_summ = minutes / 60 * rec.price
            rec.summ = all_summ

    @api.model
    def default_get(self, fields_list):
        val = super(TmBilling, self).default_get(fields_list)
        employee = self.env['sg.tm.employee'].search([('user_id',
                                                     '=', self.env.user.id)])
        if employee:
            val['employee_id'] = employee.id
        start_date = datetime.datetime.now().\
            replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        val['start_date'] = start_date
        date_now = datetime.datetime.now()
        days = monthrange(date_now.year, date_now.month)[1]
        end_date = start_date.\
            replace(day=days, hour=23, minute=59, second=59)
        val['end_date'] = end_date
        return val
