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
from openerp.osv import fields, orm

class qc_link(orm.Model):
    """
    This model is used to manage available models to link in the Reference
    fields of qc.inspection and qc.test
    """
    _name = 'qc.link'
    _description = "Test reference types"
    _order = 'priority'

    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'object': fields.char('Object', size=64, required=True),
        'priority': fields.integer('Priority'),
    }

    _defaults = {
        'priority': 5,
    }

    def get_qc_links(self, cr, uid, context=None):
        """
        Returns a list of tuples of 'model names' and 'Model title' to use as
        types in reference fields.
        """
        ids = self.search(cr, uid, [], context=context)
        res = self.read(cr, uid, ids, ['object', 'name'], context=context)
        return [(r['object'], r['name']) for r in res]
