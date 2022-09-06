from odoo.tests.common import TransactionCase
from odoo import fields


class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()
        self.group_tm_user = self.env.ref(
            'sg_task_management.group_tm_user')
        self.group_tm_admin = self.env.ref(
            'sg_task_management.group_tm_admin')
        self.tm_user = self.env['res.users'].create({
            'name': 'TM User',
            'login': 'TM_user',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_tm_user.id)],
        })
        self.tm_admin = self.env['res.users'].create({
            'name': 'TM Admin',
            'login': 'TM',
            'groups_id': [(4, self.env.ref('base.group_system').id),
                          (4, self.group_tm_admin.id)],
        })
        self.status = 'new'
        self.currency = self.env['res.currency'].create({'name': 'TEST',
                                                        'symbol': 'T'})
        self.employee_user = self.env['sg.tm.employee'].create({
            'name': 'Demo Employee User',
            'user_id': self.tm_user.id})
        self.employee_admin = self.env['sg.tm.employee'].create({
            'name': 'Demo Employee Admin',
            'user_id': self.tm_admin.id})
        self.partner = self.env['res.partner'].create({
            'name': 'Demo Partner'})
        self.project = self.env['sg.tm.project'].create({
            'name': 'Demo Project',
            'partner_id': self.partner.id})
        self.task = self.env['sg.tm.task'].create({
            'name': 'Demo Task',
            'project_id': self.project.id,
            'responsible_id': self.employee_admin.id,
            'partner_id': self.partner.id,
            'status': self.status,
            'task_date': fields.Date.today(),
            'time_total': 0,
            'time_all': 0})
        self.billing = self.env['sg.tm.billing'].create({
            'name': 'Demo Balling',
            'project_id': self.project.id,
            'employee_id': self.employee_admin.id,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today()})
        self.price = self.env['sg.tm.price'].create({
            'name': 'Test Price',
            'partner_id': self.partner.id,
            'employee_id': self.employee_admin.id,
            'price': 200,
            'currency_id': self.currency.id})
        self.task_history = self.env['sg.tm.task.history'].create({
            'task_id': self.task.id,
            'responsible_id': self.employee_admin.id,
            'number_of_minut': 200,
            'partner_id': self.partner.id,
        })
