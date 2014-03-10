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
from openerp.tools.translate import _
from openerp import netsvc
from openerp import SUPERUSER_ID

class stock_move(orm.Model):
    _inherit = 'stock.move'

    _columns = {
        'inspection_ids': fields.one2many(
                'qc.inspection', 'res_id', 'QC inspections',
                domain=[('object_id', 'like', 'stock.move,')],
                help="Defines the QC inspections this move must pass."),
    }

    def action_done(self, cr, uid, ids, context=None):
        res = super(stock_move, self).action_done(cr, uid, ids,
                                                     context=context)
        input_trigger_id = self.pool['qc.trigger'].search(cr, uid,
                    [('code', '=', 'stock_move_in')], context=context)
        if input_trigger_id:
            input_trigger_id = input_trigger_id[0]
            for move in self.browse(cr, uid, ids, context=context):
                do_inspection = False
                if not move.picking_id or move.picking_id.type != 'in':
                    continue
                for test_trigger in move.product_id.qc_test_trigger_ids:
                    if test_trigger.trigger_id.id == input_trigger_id:
                        do_inspection = True
                if do_inspection:
                    self._create_qc_inspection_from_move(cr, uid, move,
                                    input_trigger_id, context=context)
                    # Back to waiting state until inspections will be done
                    self.write(cr, uid, [move.id], {'state': 'waiting'},
                               context=context)
        return res

    def _calc_qc_inspection_vals(self, cr, uid, move, context=None):
        """
        Prepare data to create a qc.test instance related to a stock move
        @param move: Browse object of stock.move
        @return: Dictionary of stock.move values
        """
        return {
            'object_id': 'stock.move,%d' % move.id,
            'product_id': move.product_id.id,
            'product_qty': move.product_qty,
            'blocked': True,
        }

    def _create_qc_inspection_from_move(self, cr, uid, move, trigger_id,
            context=None):
        """
        Create and write into stock move QC inspections corresponding to a
        supplied trigger, getting QC test from the product of the move.
        @param move: Browse object of stock.move instance
        @param trigger_id: ID of qc.trigger instance
        @return: Boolean depending if inspections have been created or not
        """
        qc_inspection_obj = self.pool['qc.inspection']
        inspection_ids = []
        # TODO: Añadir aquí la búsqueda para los tests de compañía
        for test_trigger in move.product_id.qc_test_trigger_ids:
            if test_trigger.trigger_id.id != trigger_id:
                continue
            vals = self._calc_qc_inspection_vals(cr, uid, move,
                                                  context=context)
            inspection_id = qc_inspection_obj.create(cr, SUPERUSER_ID, vals,
                                                     context=context)
            qc_inspection_obj.set_test(cr, SUPERUSER_ID, [inspection_id],
                    test_trigger.test_id.id, context=context)
            inspection_ids.append(inspection_id)
        self.write(cr, SUPERUSER_ID, move.id,
                   {'inspection_ids': [(6, 0, inspection_ids)]},
                   context=context)
        return bool(inspection_ids)
