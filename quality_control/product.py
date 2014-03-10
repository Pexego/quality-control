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

class product_qc_trigger_template(orm.Model):
    '''
    Model to configure quality control tests triggers by product.
    Define the test to use for a trigger, ordering it by sequence.
    '''
    _name = 'product.qc.trigger.test'
    _description = 'Product QC test trigger'
    _order = 'product_id, company_id'

    _columns = {
        'product_id': fields.many2one('product.product', 'Product',
                required=True),
        'trigger_id': fields.many2one('qc.trigger', 'Trigger', required=True,
                help="The quality control trigger tag which defines for what "
                "event a quality inspection must be done."),
        'test_id': fields.many2one('qc.test', 'Test', required=True,
                help="Quality control test to be used in inspections."),
        'company_id': fields.many2one('res.company', 'Company'),
    }

    _defaults = {
        'company_id': lambda self, cr, uid, c: (
            self.pool['res.company']._company_default_get(cr, uid,
                                'product.qc.trigger.test', context=c)),
    }


class product_product(orm.Model):
    ''' Adds  a one2many field to the model to the Product which links 
    QC tests for certain triggers.'''
    _inherit = 'product.product'

    def _calc_trigger_ids(self, cr, uid, ids, fieldname, args, context=None):
        # TODO: Eliminar este método, que tampoco aporta mucho
        prod_trigger_obj = self.pool['product.qc.trigger.test']
        res = {}
        for product_id in ids:
            res[product_id] = []
            trigger_template_ids = prod_trigger_obj.search(cr, uid,
                        [('product_id', '=', product_id)], context=context)
            for trigger_template in prod_trigger_obj.browse(cr, uid,
                    trigger_template_ids, context=context):
                if trigger_template.trigger_id.id not in res[product_id]:
                    res[product_id].append(trigger_template.trigger_id.id)
        return res

    def _search_trigger_ids(self, cr, uid, obj, name, args, context):
        trigger_template_proxy = self.pool['product.qc.trigger.test']
        res = []
        for unused, operator, condition in args:
            opposite = False
            if 'in' in operator:
                if operator == 'not in':
                    operator = 'in'
                    opposite = True
            else:
                if operator in ('!=', '<>'):
                    operator = '='
                    opposite = True
            template_trigger_ids = trigger_template_proxy.search(cr, uid, [
                        ('trigger_id', operator, condition),
                    ], context=context)
            product_ids = []
            for template_trigger in trigger_template_proxy.browse(cr, uid,
                    template_trigger_ids, context):
                product_ids.append(template_trigger.product_id.id)
            operator = 'in'
            if opposite:
                operator = 'not in'
            res.append(('id', operator, product_ids))
        return res

    _columns = {
        'qc_test_trigger_ids': fields.one2many(
                'product.qc.trigger.test', 'product_id', 'QC triggers > tests',
                help="Defines when a product must to pass a quality "
                "control test for certain operation.\n"),
        'qc_trigger_ids': fields.function(_calc_trigger_ids, method=True,
                type='many2many', relation='qc.trigger', string='QC triggers',
                fnct_search=_search_trigger_ids),
    }

    def _default_qc_template_trigger_ids(self, cr, uid, context=None):
        # TODO: Esto no debería añadirse en los nuevos productos, si no cuando
        # se va a hacer el movimiento, mirar los tests que son de empresa
        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        res = []
        return res
        for company_trigger in user.company_id.qc_test_trigger_ids:
            res.append({
                'trigger_id': company_trigger.trigger_id.id,
                'template_id': company_trigger.template_id.id,
                'company_id': user.company_id.id,
            })
        return res

    _defaults = {
        'qc_test_trigger_ids': _default_qc_template_trigger_ids,
    }
