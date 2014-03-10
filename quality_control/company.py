# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, fields


class res_company_qc_trigger_template(orm.Model):
    '''
    Model to configure the default Quality Control Templates/Tests triggers by
    Company. Define the template to use for a trigger, ordering it by sequence.
    '''
    _name = 'res.company.qc.trigger.template'
    _description = 'Quality Control Template Triggers by Company'

    # TODO: Ver si conviene unificar los dos modelos: producto y compañía
    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'trigger_id': fields.many2one('qc.trigger', 'Trigger', required=True,
                help="The Quality Control Trigger Tag which defines when must "
                "to be created a Test (using the specified template) for a "
                "Production Lot."),
        'template_id': fields.many2one('qc.test', 'Test', required=True,
                                help="The Quality Control Template to use."),
    }


class res_company(orm.Model):
    '''
    Adds to the company a one2many field to the model which configures Quality
    Control Templates/Tests triggers.
    It will be used as default values when a new Product is created.
    '''
    _inherit = 'res.company'

    _columns = {
        'qc_template_trigger_ids': fields.one2many(
                'res.company.qc.trigger.template', 'company_id', 'QC Triggers',
                help="Defines when a Production Lot must to pass a Quality "
                "Control Test (based on the defined Template).\n"
                "It defines the default Template Triggers which will be used "
                "when a Product is created. Only the Product's field define "
                "the final behavior of its lots: which template to use or "
                "don't require any test if there aren't any trigger defined."),
    }
