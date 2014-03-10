## -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, orm
import decimal_precision as dp

class qc_test(orm.Model):
    _name = 'qc.test'
    _description = 'Quality test'

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if 'name' not in vals and vals.get('object_id'):
            ctx = context.copy()
            ref_model, ref_id = vals['object_id'].split(',')
            ctx['reference_model'] = ref_model
            ctx['reference_id'] = long(ref_id)
            vals['name'] = self._default_name(cr, uid, context=ctx)
        return super(qc_test, self).create(cr, uid, vals, context=context)

    def _default_name(self, cr, uid, context=None):
        if context and context.get('reference_model'):
            ref_id = context.get('reference_id')
            if not ref_id:
                ref_id = context.get('active_id')
            if ref_id:
                source = self.pool.get(context['reference_model']).browse(cr,
                        uid, ref_id, context)
                if hasattr(source, 'name'):
                    return source.name
        return False

    def _default_object_id(self, cr, uid, context=None):
        if context and context.get('reference_model', False):
            return '%s,%d' % (context['reference_model'],
                    context['reference_id'])
        return False

    def _default_type(self, cr, uid, context=None):
        if context and context.get('reference_model'):
            return 'related'
        return False

    _columns = {
        'active': fields.boolean('Active', select=True),
        'name': fields.char('Name', size=200, required=True, translate=True,
                select=True),
        'line_ids': fields.one2many('qc.test.line',
                'test_id', 'Lines'),
        'object_id': fields.reference('Reference object', size=128,
                selection=lambda s, cr, uid, context=None: s.pool['qc.link']\
                                    .get_qc_links(cr, uid, context=context)),
        'fill_correct_values': fields.boolean('Fill with correct values?'),
        'type': fields.selection([
                    ('generic', 'Generic'),
                    ('related', 'Related'),
                ], 'Type', select=True),
        'formula': fields.text('Formula'),
        'company_id': fields.many2one('res.company', 'Company'),
        'uom_id': fields.many2one('product.uom', 'UoM'),
    }

    _defaults = {
        'name': _default_name,
        'active': True,
        'object_id': _default_object_id,
        'type': _default_type,
        'company_id': lambda s, cr, uid, context=None:
                s.pool.get('res.company')._company_default_get(cr, uid,
                        'qc.test', context=context),
    }


class qc_test_line(orm.Model):
    _name = 'qc.test.line'

    def onchange_question_id(self, cr, uid, ids, question_id, context=None):
        res = {}
        if question_id:
            question = self.pool['qc.question'].browse(cr, uid, question_id,
                                                       context=context)
            if question:
                res['value'] = {'type': question.type}
                #TODO: Reset qualitative or quantitative data as needed
        return res

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'sequence': fields.integer('Sequence', required=True),
        'test_id': fields.many2one('qc.test',
                'Quality test', select=True),
        'question_id': fields.many2one('qc.question', 'Question',
                                       required=True, select=True),
        'valid_value_ids': fields.many2many('qc.answer',
                'qc_test_value_rel', 'test_line_id', 'value_id',
                'Valid answers'),
        'notes': fields.text('Notes'),
        ###### Only if quantitative ########
        'min_value': fields.float('Min',
                digits_compute=dp.get_precision('Quality control')),
        'max_value': fields.float('Max',
                digits_compute=dp.get_precision('Quality control')),
        'uom_id': fields.many2one('product.uom', 'UoM'),
        ####################################
        'question_type': fields.related('question_id', 'type',
                type='selection', string='Type', readonly=True, store=True,
                selection=[('qualitative', 'Qualitative'),
                           ('quantitative', 'Quantitative')]),
        'company_id': fields.related('test_id', 'company_id',
                type='many2one', relation='res.company', string='Company',
                store=True, readonly=True),
    }

    _defaults = {
        'sequence': 10,
    }

    _order = "sequence, name"