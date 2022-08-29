from odoo import models, fields, api


class TmBilling(models.Model):
    """Сalculation of revenue for completed tasks
    """
    _name = 'sg.tm.billing'
    _description = 'Billing'
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    project_id = fields.Many2one(comodel_name='sg.tm.project',
                                 required=True)
    partner_id = fields.Many2one(comodel_name='res.partner',
                                 readonly=True,
                                 compute='_compute_get_price_partner')
    currency_id = fields.Many2one(comodel_name='res.currency',
                                  string='Currency',
                                  store=True,
                                  readonly=True,
                                  compute='_compute_get_price_partner',
                                  help="The payment's currency.")
    price = fields.Monetary(currency_field='currency_id',
                            compute='_compute_get_price_partner')
    summ = fields.Monetary(currency_field='currency_id',
                           compute='_compute_summ')
    employee_id = fields.Many2one(comodel_name='sg.tm.employee',
                                  required=True)

    @api.depends('project_id', 'employee_id')
    def _compute_get_price_partner(self):
        """The method finds the price by the "project_id"
        and "employee_id fields,
        and also finds the partner and currency.
        :param notify_type: none
        :return None:
        """
        for rec in self:
            if rec.project_id.id:
                rec.partner_id = rec.project_id.partner_id.id
                if rec.employee_id.id:
                    price_id = self.env['sg.tm.price'].search([
                        ('partner_id', '=', rec.partner_id.id),
                        ('employee_id', '=', rec.employee_id.id)])
                    if price_id:
                        rec.price = price_id.price
                        rec.currency_id = price_id.currency_id.id
                    else:
                        rec.price = 0
                        rec.currency_id = 0
                else:
                    rec.price = 0
                    rec.currency_id = 0
            else:
                rec.partner_id = 0
                rec.price = 0
                rec.currency_id = 0

    @api.depends('project_id', 'employee_id', 'start_date', 'end_date')
    def _compute_summ(self):
        """The method finds all completed tasks for the specified period
        and calculates the total cost.
        :param notify_type: none
        :return None:
        """
        for rec in self:
            if rec.project_id and rec.employee_id and rec.start_date \
                    and rec.end_date:
                task_history_ids = self.env['sg.tm.task.history'].search([
                    ('partner_id', '=', rec.partner_id.id),
                    ('responsible_id', '=', rec.employee_id.id),
                    ('task_id.status', '=', 'done'),
                    ('record_date', '>=', rec.start_date),
                    ('record_date', '<=', rec.end_date)])
                if task_history_ids:
                    minutes = 0
                    for task_history in task_history_ids:
                        minutes += task_history.number_of_minut
                    summ = minutes / 60 * rec.price
                    rec.summ = summ
                else:
                    rec.summ = 0
            else:
                rec.summ = 0

    @api.model
    def default_get(self, fields_list):
        val = super(TmBilling, self).default_get(fields_list)
        partner = self.env['sg.tm.employee'].search([('user_id',
                                                     '=', self.env.user.id)])
        if partner:
            val['employee_id'] = partner.id
        return val
