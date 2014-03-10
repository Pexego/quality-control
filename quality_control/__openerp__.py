# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) All Rights Reserved.
#        2010-2011: NaN Projectes de Programari Lliure, S.L.
#                   http://www.NaN-tic.com
#        2014:      Serv. Tecnol. Avanzados - Pedro M. Baeza
#                   http://www.serviciosbaeza.com
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

{
    "name": "Quality control",
    "version": "1.0",
    "author": "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "website": "http://www.serviciosbaeza.com",
    "category": "Quality control",
    "description": """
Quality control module for OpenERP
==================================

This module is generic. It's the basis for an automatically integration with
different models of the application. However, it allows also to make any
quality control at the different models of the system manually.

Definition:

* Question: The thing to be checked. We have two types of questions:

 * Qualitative: The result is a description, color, yes, no...
 * Quantitative: The result must be within a range.

* Possible values: The values chosen in qualitative questions.

* Test: The set of questions to be used in inspections.

* Once these values are set, we define the test.

We have a *generic* test that can be applied to any model: shipments,
invoices or product, or a *test related*, making it specific to a particular
product and that eg apply whenever food is sold or when creating a batch.

Once these parameters are set, we can just pass the test. We create a
new inspection, selecting a relationship with the model (sale, stock move...),
and pressing "Select test" button to choose the test to pass. Then, you must
fill the lines depending on the chosen test.

The complete inspection workflow is:

    Draft -> Confirmed -> Success
                |
                | -> Failure (Pending approval) -> Approved

Based on the nan_quality_control_* modules from NaN·tic.
    """,
    "depends": [
        'product'
    ],
    "images": [
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'quality_control_view.xml',
        'wizard/qc_inspection_set_test_view.xml',
        'qc_question_view.xml',
        'qc_answer_view.xml',
        'qc_test_view.xml',
        'qc_inspection_view.xml',
        'qc_inspection_workflow.xml',
        'product_view.xml',
        #'company_view.xml',
        'quality_control_data.xml',
    ],
    "installable": True,
}
