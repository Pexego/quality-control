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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, fields
from openerp.tools.translate import _


class qc_trigger(orm.Model):
    _name = 'qc.trigger'
    _description = 'Quality control trigger tag'

    _columns = {
        'code': fields.char('Code', size=30, required=True),
        'name': fields.char('Name', size=128, required=True, translate=True),
        'location_id': fields.many2one('stock.location', 'Source Location', required=False, help="Source location for triggering."),
        'location_dest_id': fields.many2one('stock.location', 'Destination Location', required=False, help="Destination location for triggering."),
        'journal_id': fields.many2one('stock.journal', 'Stock Journal', required=False, help="Stock journal for triggering."),
        'picking_type': fields.selection([('out', 'Sending Goods'), ('in', 'Getting Goods'), ('internal', 'Internal')], 'Picking Type'),

    }

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         _("The code of the quality control trigger tag must be unique!")),
    ]