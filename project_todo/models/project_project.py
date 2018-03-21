# -*- coding: utf-8 -*-
# © 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
import datetime

class ProjectProject(models.Model):
    _inherit = 'project.project'

    todo_count = fields.Integer(compute='_compute_task_count')
    associated_todos = fields.Many2many('project.todo')
    color = fields.Integer(required=True)
    sequence = fields.Integer(default = 44)   


    @api.multi
    @api.depends('associated_todos')
    def _compute_todo_count(self):
        for this in self:
            # acrive record interface activated in compute funcs
            this.todo_count = len(this.associated_todos)

    @api.multi
    @api.depends('associated_todos')
    def _compute_task_count(self):    	
   		res=super(ProjectProject, self)._compute_task_count()
   		for this in self:
   			this.todo_count = len(this.associated_todos)


    @api.multi
    def write(self, vals):
        #call parent write
        for this in self:
            # if there are associated todos sequence is 1
            if this.associated_todos:
                vals['sequence'] = 1
            res = super(ProjectProject, this).write(vals)
        return res


    @api.model
    def create(self, vals):
        #call parent create
        res = super(ProjectProject, self).create(vals)
        # dosomething!
        # NOTE: no active record pattern here!
        # monochrome  projects!
        res.write({'color' : 5})
        return res


