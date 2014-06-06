## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">
        ${css}

.list_main_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
table.list_main_table {
    margin-top: 20px;
}
.list_main_headers {
    padding: 0;
}
.list_main_headers th {
    border: thin solid #000000;
    padding-right:3px;
    padding-left:3px;
    background-color: #EEEEEE;
    text-align:center;
    font-size:12;
    font-weight:bold;
}
.list_main_table td {
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_main_lines,
.list_main_footers {
    padding: 0;
}
.list_main_footers {
    padding-top: 15px;
}
.list_main_lines td,
.list_main_footers td,
.list_main_footers th {
    border-style: none;
    text-align:left;
    font-size:12;
    padding:0;
}
.list_main_footers th {
    text-align:left;
}

td .total_empty_cell {
    width: 50%;
}
td .total_sum_cell {
    width: 50%;
}

.nobreak {
    page-break-inside: avoid;
}
caption.formatted_note {
    text-align:left;
    border-right:thin solid #EEEEEE;
    border-left:thin solid #EEEEEE;
    border-top:thin solid #EEEEEE;
    padding-left:10px;
    font-size:11;
    caption-side: bottom;
}
caption.formatted_note p {
    margin: 0;
}

.main_col1 {
    width: 40%;
}
td.main_col1 {
    text-align:left;
}
.main_col2,
.main_col3,
.main_col4,
.main_col6 {
    width: 10%;
}
.main_col5 {
    width: 7%;
}
td.main_col5 {
    text-align: center;
    font-style:italic;
    font-size: 10;
}
.main_col7 {
    width: 13%;
}

.right_table {
    right: 4cm;
    width:"100%";
}

.std_text {
    font-size:12;
}

th.date {
    width: 90px;
}

td.amount, th.amount {
    text-align: right;
    white-space: nowrap;
}

td.date {
    white-space: nowrap;
    width: 90px;
}

.address .recipient .shipping .invoice {
    font-size: 12px;
}

    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    <%def name="address(partner)">
        <%doc>
            XXX add a helper for address in report_webkit module as this won't be suported in v8.0
        </%doc>
        %if partner.parent_id:
            <tr><td class="name">${partner.parent_id.name or ''}</td></tr>
            <tr><td>${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n")[1:] %>
        %else:
            <tr><td class="name">${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n") %>
        %endif
        %for part in address_lines:
            % if part:
                <tr><td>${part}</td></tr>
            % endif
        %endfor
    </%def>

    %for inspection in objects:
    
   <div class="address">
        <table class="recipient">
          
        </table>

    </div>

    <h1 style="clear:both;">${inspection.test_id.name}</h1>
    <h1 style="clear:both;">${inspection.object_id.name} ${inspection.object_id.origin or '' } ${inspection.object_id.picking_id and inspection.object_id.picking_id.name  or '' }</h1>

    <table class="basic_table" width="100%">
        <tr>
            <th class="date">${_("Referencia")}</td>
            <th>${_("Fecha")}</td>
            <th>${_("Producto")}</td>
            <th>${_('Cantidad')}</td>
	    <th>${_('Lote')}</td>
        </tr>
        <tr>
	    <td>${inspection.name or ''}</td>
            <td class="date">${formatLang(inspection.date, date=True)}</td>
            
            <td>${inspection.product_id and inspection.product_id.name or ''}</td>
            <td>${ formatLang(inspection.product_qty ) }</td>
            <td>${inspection.object_id and inspection.object_id.prodlot_id and inspection.object_id.prodlot_id.name or ''}</td>
        </tr>
    </table>

    <table class="list_main_table" width="100%">
      <thead>
        <tr>
          <th class="list_main_headers" style="width: 100%">
            <table style="width:100%">
              <tr>
                <th class="main_col1">${_("Nombre")}</th>
                <th class="main_col1">${_("Valor")}</th>
		<th class="main_col1">${_("Notas")}</th>
                
              </tr>
            </table>
          </th>
        </tr>
      </thead>
      <tbody>
        %for line in inspection.line_ids:
          <tr>
            <td class="list_main_lines" style="width: 100%">
              <div class="nobreak">
                <table style="width:100%">
                  <tr>
                    <td class="main_col1">${ line.name }</td>
		     %if line.actual_value_qt:
                    <td class="main_col1">${ formatLang(line.actual_value_qt ) or '' }</td>
                    %endif
		     %if line.actual_value_ql:
                    <td class="main_col1">${ line.actual_value_ql.name or ''  }</td>
                    %endif
		    <td class="main_col1">${ line.notes or '' }</td>
                  </tr>
                 </table>
              </div>
            </td>
          </tr>
        %endfor
      </tbody>
    </table>
    <table>
        <tr>
          <td class="list_main_footers" style="width: 100%">
            <div class="nobreak">
              <table style="width:100%">
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Notas internas:")}
                  </th>
                  <td class="amount total_sum_cell">
                    ${inspection.internal_notes or ''}
                  </td>
                </tr>
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Notas externas:")}
                  </th>
                  <td class="amount total_sum_cell">
                    ${inspection.external_notes or ''}
                  </td>
                </tr>
             
              </table>
            </div>
          </td>
        </tr>
    </table>


    %endfor
</body>
</html>
