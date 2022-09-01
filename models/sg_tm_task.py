from odoo import models, fields, api, _
import datetime


class TmTask(models.Model):
    """Used to create a task and further work with them
    """
    _name = 'sg.tm.task'
    _description = 'Task'
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    project_id = fields.Many2one(comodel_name='sg.tm.project',
                                 required=True)
    author_id = fields.Many2one(comodel_name='res.users',
                                readonly=True)
    responsible_id = fields.Many2one(comodel_name='sg.tm.employee',
                                     required=True)
    status = fields.Selection([('new', _('New')),
                               ('in_work', _('In work')),
                               ('testing', _('Testing')),
                               ('done', _('Done'))],
                              required=True)
    partner_id = fields.Many2one(comodel_name='res.partner',
                                 compute='_compute_partner_id',
                                 store=True)
    task_date = fields.Date(string='Date',
                            default=fields.Date.today,
                            required=True)
    number_of_minut = fields.Integer(string='Duration',
                                     compute='_compute_time',
                                     readonly=False)
    time_total = fields.Integer(string='Responsible time',
                                compute='_compute_total_time',
                                readonly=True,
                                store=True)
    time_all = fields.Integer(string='All time',
                            compute='_compute_total_time',
                            readonly=True,
                            store=True)
    description = fields.Text()
    color = fields.Integer()
    task_history_ids = fields.One2many(comodel_name='sg.tm.task.history',
                                       inverse_name='task_id')
    comment = fields.Char(zise=100)
    
    @api.depends('number_of_minut')
    def _compute_total_time(self):
        for rec in self:
            task_history_ids = rec._return_task_history(rec.ids)
            total = 0
            all = 0
            for task_history_id in task_history_ids:  
                all += task_history_id.number_of_minut
                if task_history_id.responsible_id.id == rec.responsible_id.id:
                    total += task_history_id.number_of_minut   
            rec.time_total = total
            rec.time_all = all

    def _return_task_history(self, record_id, responsible_id=0):
        """Function searches and returns an record "sg.tm.task.history"
        :param notify_type: can have two value "record_id" or "responsible_id",
        :return record "sg.tm.task.history"
        """
        domain = [('task_id','=', record_id)]
        if responsible_id != 0:
            domain = [('task_id','=', record_id),
                    ('responsible_id','=', responsible_id)]   
        return self.env['sg.tm.task.history'].search(domain)

    def _create_task_history(self, name, task_id, responsible_id,
                             number_of_minut, partner_id, status,
                             comment):
        """Creates a new record sg.tm.task.history
        :param notify_type: can have five value
        "name", "task_id", "responsible_id", "number_of_minut",
        "partner_id"
        :return none
        """
        self.env['sg.tm.task.history'].create({
            'name': name,
            'record_time': datetime.datetime.now(),
            'task_id': task_id,
            'responsible_id': responsible_id,
            'number_of_minut': number_of_minut,
            'partner_id': partner_id,
            'status': status,
            'comment': comment,
        })

    @api.depends('project_id')
    def _compute_partner_id(self):
        for rec in self:
            if rec.project_id:
                rec.partner_id = rec.project_id.partner_id.id
            else:
                rec.partner_id = 0

    @api.depends('responsible_id')
    def _compute_time(self):
        """Returns the number of minutes if a record with the key
        fields already exists
        :param notify_type: none
        :return none
        """
        for rec in self:
            rec.number_of_minut = 0
            rec.comment = ''

    @api.model
    def default_get(self, fields_list):
        val = super(TmTask, self).default_get(fields_list)
        val['author_id'] = self.env.user.id
        val['status'] = 'new'
        return val

    @api.model
    def create(self, vals):
        """Creates a new entry in task_history
        :param notify_type: vals - the value of the fields that have changed
        :return none
        """
        new_record = super().create(vals)
        if 'responsible_id' in vals:
            self._create_task_history(new_record.name,
                                      new_record.id,
                                      vals.get('responsible_id'),
                                      vals.get('number_of_minut'),
                                      new_record.partner_id.id,
                                      new_record.status,
                                      new_record.comment)
        return new_record

    def write(self, vals):
        """Searches for and modifies the task_history entry by key fields,
        or creates a new entry if not found.
        The write occurs only if the "number_of_minute" (compute)
        field changes. If the owner changes,
        a record is created with the owner before the change.
        :param notify_type: vals - the value of the fields that have changed
        :return TmTask
        """
        if 'number_of_minut' not in vals and 'status' not in vals:
            return super().write(vals)
        for record in self:
            is_create_task_history = False
            responsible_id = record.responsible_id.id
            status = record.status
            number_of_minut = record.number_of_minut
            comment = record.comment
            for key, value in vals.items():
                if key == 'status':
                    status = value
                elif key == 'number_of_minut':
                    number_of_minut = value
                elif key == 'responsible_id':
                    responsible_id = value
                elif key == 'comment':
                    comment = value       
            if 'status' in vals and len(vals) == 1:
                number_of_minut = 0
                is_create_task_history = True
            else:
                is_create_task_history = True
            if is_create_task_history:
                self._create_task_history(record.name,
                                          record.id,
                                          responsible_id,
                                          number_of_minut,
                                          record.partner_id.id,
                                          status,
                                          comment)
        super().write(vals)
        return True