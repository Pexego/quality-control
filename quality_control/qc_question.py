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

class qc_question(orm.Model):
    """
    This model stores proofs which will be part of a test. Proofs are
    classified between qualitative (such as color) and quantitative
    (such as density).
    """
    _name = 'qc.question'

    _columns = {
        'name': fields.char('Name', size=200, required=True, select=True,
                translate=True),
        'ref': fields.char('Code', size=30, select=True),
        'type': fields.selection([('qualitative', 'Qualitative'),
                                  ('quantitative', 'Quantitative')],
                                  'Type', select=True, required=True),
        'value_ids': fields.many2many('qc.answer',
                'qc_answer_rel', 'question_id', 'answer_id',
                'Possible answers'),
        'company_id': fields.many2one('res.company', 'Company'),
    }

    _defaults = {
        'company_id': lambda self, cr, uid, c:
                self.pool.get('res.company')._company_default_get(cr, uid,
                        'qc.question', context=c),
    }
