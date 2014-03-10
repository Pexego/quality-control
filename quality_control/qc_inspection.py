# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from decimal import Decimal
import openerp.addons.decimal_precision as dp
import time

class qc_inspection(orm.Model):
    _name = 'qc.inspection'

    def _get_success(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for inspection in self.browse(cr, uid, ids, context):
            success = True
            for line in inspection.line_ids:
                success = success and line.success
            result[inspection.id] = success
        return result

    def _get_res_id(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for inspection in self.browse(cr, uid, ids, context):
            result[inspection.id] = (inspection.object_id and
                                     inspection.object_id.id or False)
        return result

    def _default_object_id(self, cr, uid, context=None):
        if context and context.get('reference_model', False):
            return '%s,%d' % (
                    context['reference_model'],
                    context['reference_id'])
        return False

    _columns = {
        'name': fields.char('Number', size=64, required=True, select=True),
        'date': fields.datetime('Date', required=True, readonly=True,
                select=True, states={
                    'draft': [('readonly', False)],
                }),
        'object_id': fields.reference('Reference',
                size=128, readonly=True, select=True,
                states={'draft': [('readonly', False)]},
                selection=lambda s, cr, uid, context=None: s.pool['qc.link']\
                                    .get_qc_links(cr, uid, context=context)),
        'res_id': fields.function(_get_res_id, method=True, type='integer',
                string='Resource ID', select=True, store=True, readonly=True),
        'product_id': fields.many2one('product.product', 'Product',
                select=True, domain=[('type','<>','service')], readonly=True,
                states={'draft': [('readonly', False)]}),
        'product_qty': fields.float('Quantity', readonly=True,
            digits_compute=dp.get_precision('Product Unit of Measure'),
            states={'draft': [('readonly', False)]}),
        'test_id': fields.many2one('qc.test', 'Test',
                select=True, states={
                    'success': [('readonly', True)],
                    'failed': [('readonly', True)],
                }),
        'line_ids': fields.one2many('qc.inspection.line', 'inspection_id',
                'Inspection lines', states={
                    'success': [('readonly', True)],
                    'failed': [('readonly', True)],
                }),
        'internal_notes': fields.text('Internal notes'),
        'external_notes': fields.text('External notes', states={
                    'success': [('readonly', True)],
                    'failed': [('readonly', True)],
                }),
        'state': fields.selection([
                ('draft', 'Draft'),
                ('waiting', 'Waiting answers'),
                ('success', 'Inspection succcess'),
                ('failed', 'Inspection failed'),
                ('approved', 'Approved by supervisor'),
            ], 'State', readonly=True, select=True),
        'success': fields.function(_get_success, method=True, type='boolean',
                string='Success', select=True, store=True,
                help='This field will be true if all tests have succeeded.'),
        'company_id': fields.many2one('res.company', 'Company'),
        'blocked': fields.boolean('Blocked', help="If this field is set, it "
                "means that the inspection has been generated from an "
                "automatic process and cannot be cancelled."),
    }

    _defaults = {
        'name': lambda s, cr, uid, context=None: \
                s.pool['ir.sequence'].get(cr, uid, 'qc.inspection',
                                          context=context),
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'blocked': False,
        'state': 'draft',
        'success': False,
        'object_id': _default_object_id,
        'company_id': lambda s, cr, uid, context=None: s.pool['res.company']\
            ._company_default_get(cr, uid, 'qc.inspection', context=context),
    }

    def _calc_line_vals_from_test_line(self, cr, uid, inspection_id,
                        test_line, fill=False, context=None):
        data = {
            'name': test_line.name,
            'inspection_id': inspection_id,
            'test_line_id': test_line.id,
            'notes': test_line.notes,
        }
        if fill:
            if test_line.question_type == 'qualitative':
                # Fill with the first correct value found.
                data['actual_value_ql'] = (test_line.valid_value_ids
                        and test_line.valid_value_ids[0]
                        and test_line.valid_value_ids[0].id
                        or False)
            else:
                # Fill with a value in the range (min value
                data['actual_value_qt'] = test_line.min_value
        return data

    def set_test(self, cr, uid, ids, test_id, force_fill=False, context=None):
        insp_line_obj = self.pool['qc.inspection.line']
        test = self.pool['qc.test'].browse(cr, uid, test_id, context=context)
        for inspection in self.browse(cr, uid, ids, context=context):
            if inspection.line_ids:
                insp_line_obj.unlink(cr, uid,
                                     [x.id for x in inspection.line_ids],
                                     context=context)
            self.write(cr, uid, inspection.id, {'test_id': test_id},
                       context=context)
            fill = test.fill_correct_values
            lines = []
            for line in test.line_ids:
                data = self._calc_line_vals_from_test_line(cr, uid,
                    inspection.id, line, context=context,
                    fill=test.fill_correct_values or force_fill)
                lines.append(data)
            self.write(cr, uid, inspection.id,
                       {'line_ids': [(0, 0, line) for line in lines]},
                       context=context)
        return True

    def test_state(self, cr, uid, ids, mode, context):
        '''Currently not used.'''
        quality_check = False
        if mode == 'failed':
            return not quality_check
        if mode == 'success':
            return quality_check
        return False

    def action_workflow_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
                    'state': 'draft'
                }, context=context)
        return True

    def action_workflow_waiting(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
                    'state': 'waiting'
                }, context=context)
        return True

    def action_workflow_success(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
                    'state': 'success'
                }, context=context)
        return True

    def action_workflow_failed(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
                    'state': 'failed'
                }, context=context)
        return True

    def action_workflow_approved(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
                    'state': 'approved'
                }, context=context)
        return True

    def test_workflow_draft(self, cr, uid, ids, context=None):
        # if qc_inspection.state=='success':
        return True

    def copy(self, cr, uid, id, default=None, context=None):
        # TODO: Revisar esta duplicación
        if default is  None:
            default = {}
        if not 'name' in default:
            default['name'] = self.pool['ir.sequence'].get(cr, uid, 'qc.inspection')
        if not 'date' in default:
            #TODO: Poner formato del servidor
            default['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        return super(qc_inspection, self).copy(cr, uid, id, default=default,
                                               context=context)

    def unlink(self, cr, uid, ids, context=None):
        for inspection in self.browse(cr, uid, ids, context=context):
            if not inspection.state == 'draft':
                raise orm.except_orm(_('Error'), _("You cannot remove any "
                                "inspection that is not on draft state."))
        return super(qc_inspection, self).unlink(cr, uid, ids, context=context)

class qc_inspection_line(orm.Model):
    _name = 'qc.inspection.line'
    _rec_name = 'question_id'

    def quality_test_check(self, cr, uid, ids, field_name, field_value,
            context):
        res = {}
        lines = self.browse(cr, uid, ids, context)
        for line in lines:
            if line.question_type == 'qualitative':
                res[line.id] = self.quality_test_qualitative_check(cr, uid,
                        line, context=context)
            else:
                res[line.id] = self.quality_test_quantitative_check(cr, uid,
                        line, context=context)
        return res

    def quality_test_qualitative_check(self, cr, uid, line, context):
        return (line.actual_value_ql.id in
                [x.id for x in line.valid_value_ids])

    def quality_test_quantitative_check(self, cr, uid, line, context):
        return (line.actual_value_qt >= line.min_value and 
                line.actual_value_qt <= line.max_value)

    _columns = {
        'name': fields.char('Name', size=64, readonly=True),
        'inspection_id': fields.many2one('qc.inspection', 'inspection'),
        'test_line_id': fields.many2one('qc.test.line', 'Test line',
                                        readonly=True),
        'question_id': fields.related('test_line_id', 'question_id',
                                      type="many2one", relation='qc.question',
                                      string='Question', readonly=True),
        'valid_value_ids': fields.related('test_line_id', 'valid_value_ids',
                    type="many2many", relation='qc.answer',
                    string='Allowed values', readonly=True),
        'question_type': fields.related('test_line_id', 'question_type',
                    type="selection",string='Question type', readonly=True,
                    selection=[('qualitative', 'Qualitative'),
                               ('quantitative', 'Quantitative')]),
        'min_value': fields.related('test_line_id', 'min_value', type="float",
                string="Min", readonly=True,
                help="Minimum allowed value if it is a quantitative question."),
        'max_value': fields.related('test_line_id', 'max_value', type="float",
                string="Max", readonly=True,
                help="Maximum allowed value if it is a quantitative question."),
        'actual_value_qt': fields.float('Quant. value',
                digits_compute=dp.get_precision('Quality control'),
                help="Value of the result if it is a quantitative question."),
        'actual_value_ql': fields.many2one('qc.answer', 'Qual. value',
                help="Value of the result if it is a qualitative question."),
        'notes': fields.text('Notes', readonly=True),
        'success': fields.function(quality_test_check, type='boolean',
                method=True, string="Success?", select=True),
        'company_id': fields.related('inspection_id', 'company_id',
                type='many2one', relation='res.company', string='Company',
                store=True, readonly=True),
    }
