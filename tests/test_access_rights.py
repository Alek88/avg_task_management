from odoo.addons.sg_task_management.tests.common import TestCommon
from odoo.tests import tagged
from odoo.exceptions import AccessError
from odoo import fields


@tagged('post_install', '-at_install', 'access')
class TestAccessRights(TestCommon):

    def test_01_tm_user_access_rights(self):
        with self.assertRaises(AccessError):
            self.env['sg.tm.task'].with_user(self.tm_user).create(
                {'name': 'Demo Task 1',
                 'project_id': self.project.id,
                 'responsible_id': self.employee_admin.id,
                 'task_date': fields.Date.today()})

    def test_02_tm_user_access_rights(self):
        with self.assertRaises(AccessError):
            price = self.env['sg.tm.price'].search([('name',
                                                     '=', 'Test Price')])
            price.with_user(self.tm_user).write({'price': '1000'})

    def test_03_tm_admin_access_rights(self):
        task = self.env['sg.tm.task'].with_user(self.tm_admin).create(
            {'name': 'Demo Employee',
             'project_id': self.project.id,
             'responsible_id': self.employee_admin.id,
             'task_date': fields.Date.today()})
        task.with_user(self.tm_admin).read()
        task.with_user(self.tm_admin).write({'name': 'Demo Task 2'})
        task.with_user(self.tm_admin).unlink()
