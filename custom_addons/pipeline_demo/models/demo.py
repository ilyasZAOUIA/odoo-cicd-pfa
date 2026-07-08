from odoo import fields, models


class PipelineDemo(models.Model):
    _name = "pipeline.demo"
    _description = "Pipeline Demo"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
