from odoo.tests import tagged
from odoo.tests.common import Form
from odoo.addons.sg_task_management.tests.common import TestCommon


@tagged('post_install', '-at_install')
class TestForm(TestCommon):

    def test_1_task_default_get(self):
        task_form = Form(self.task)
        self.assertEqual(task_form.status, 'new')

    def test_2_employee_default_active(self):
        task_form = Form(self.employee_admin)
        self.assertTrue(task_form.active)

    def test_3_employee_default_user(self):
        task_form = Form(self.employee_admin)
        self.assertEqual(task_form.user_id, self.tm_admin)
