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

class qc_inspection_set_test_wizard(orm.TransientModel):
    _name = 'qc.inspection.wizard_set_test'

    def _default_test_id(self, cr, uid, context):
        test_id = context.get('active_id')
        test = self.pool['qc.inspection'].browse(cr, uid, test_id, context)
        if test:
            ids = self.pool['qc.test'].search(cr, uid, [
                        ('object_id', '=', test.object_id),
                    ], context=context)
        return ids and ids[0] or False

    _columns = {
        'test_id': fields.many2one('qc.test', 'Test'),
    }

    _defaults = {
        'test_id': _default_test_id,
    }

    def action_create_test(self, cr, uid, ids, context):
        wizard = self.browse(cr, uid, ids[0], context)
        self.pool['qc.inspection'].set_test(cr, uid, [context['active_id']],
                                            wizard.test_id.id, context=context)
        return {
            'type': 'ir.actions.act_window_close',
        }