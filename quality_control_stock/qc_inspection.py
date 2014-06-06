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

class qc_inspection(orm.Model):
    _inherit = 'qc.inspection'

    def _change_move_state(self, cr, uid, ids, context=None):
        """ Change stock moves associated to inspection to state done."""
        move_obj = self.pool['stock.move']
        for inspection in self.browse(cr, uid, ids, context=context):
            # TODO: Comprobar si se ha cancelado el movimiento
            if inspection.object_id._model._name == "stock.move":
                # Check if there is any pending test for this move
                for move_inspection in inspection.object_id.inspection_ids:
                    if not move_inspection.state in ['success', 'approved']:
                        break
                else:
                    move_obj.action_done(cr, uid, [inspection.object_id.id], context=context)
                    #move_obj.write(cr, uid, inspection.object_id.id,
                    #               {'state': 'done'}, context=context)

    def action_workflow_success(self, cr, uid, ids, context=None):
        super(qc_inspection, self).action_workflow_success(cr, uid, ids,
                                                           context=context)
        self._change_move_state(cr, uid, ids, context=context)
        return True

    def action_workflow_approved(self, cr, uid, ids, context=None):
        super(qc_inspection, self).action_workflow_approved(cr, uid, ids,
                                                           context=context)
        self._change_move_state(cr, uid, ids, context=context)
        return True
