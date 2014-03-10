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

class qc_answer(orm.Model):
    """
    This model stores all possible values of qualitative questions.
    """
    _name = 'qc.answer'

    _columns = {
        'name': fields.char('Name', size=200, required=True, select=True,
                translate=True),
        'company_id': fields.many2one('res.company', 'Company'),
    }

    _defaults = {
        'company_id': lambda self, cr, uid, c:
                self.pool.get('res.company')._company_default_get(cr, uid,
                        'qc.answer', context=c),
    }

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        if context is None:
            context = {}
        if context.get('question_id'):
            ctx = context.copy()
            del ctx['question_id']
            # TODO: check if it's possible to do:  self.search(cr, uid, [
            #             ('question_ids', 'in', [context['question_id']]),
            #         ], context=ctx)
            question = self.pool['qc.question'].browse(cr, uid,
                    context['question_id'], context=ctx)
            result = [x.id for x in question.value_ids]
            args = args[:]
            args.append(('id', 'in', result))
        return  super(qc_answer, self).search(cr, uid, args, offset,
                                              limit, order, context, count)


