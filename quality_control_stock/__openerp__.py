# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010-2012 NaN Projectes de Programari Lliure, S.L.
#                         All Rights Reserved.
#                         http://www.NaN-tic.com
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

{
    "name": "Quality control for input stock moves",
    "version": "0.2",
    "author": "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "website": "http://www.serviciosbaeza.com",
    "category": "Quality control",
    "description": """
This module supply an infrastructure to define quality tests that stock moves
must pass in some situations. It modifies stock move current workflow.

Adds a new simple model for Quality Test to define Triggers (a mark to
specify when a test must be passed) a model related to product with
one2many field which define which tests must to pass the lots of the
product specifying the Test Template and the Trigger. In the Company there
are a similar field and one2many to define the general tests (when a
product is created take the default values from these values).
In the Production Lot there are a similar model and one2many field but
relates the Lot with a trigger and Test.

IMPORTANT: This module, without anything else, doesn't define any test.
They will be defined in other dependent modules.
    """,
    "depends": [
        'stock',
        'quality_control',
    ],
    "data": [
        'qc_stock_view.xml',
        'qc_stock_data.xml',
    ],
    "images": [],
    "demo": [],
    "test": [],
    "installable": True,
    "auto_install": True,
}
