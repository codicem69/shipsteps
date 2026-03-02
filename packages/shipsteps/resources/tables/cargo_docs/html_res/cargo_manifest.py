#!/usr/bin/env python
# encoding: utf-8

from gnr.web.gnrbaseclasses import TableScriptToHtml


class Main(TableScriptToHtml):

    maintable = 'shipsteps.cargo_docs'
    #Non indicheremo una row_table ma solo una maintable perché stamperemo i record della selezione corrente
    doc_header_height = 32
    doc_footer_height = 30
    grid_header_height = 5
    page_orientation = 'landscape'
    virtual_columns = '$scn'
    css_requires='grid'

    def docHeader(self, header):
        layout = header.layout(name='doc_header', margin='5mm', border_width=0)

        row = layout.row()
        row.cell("""<center><div style='font-size:20pt;'><strong>CARGO MANIFEST</strong><br></div></center>::HTML""", width=100)
        left_cell = row.cell(width=60)
        center_cell = row.cell(width=60)
        right_cell = row.cell(width=60)
      
        self.datiLeft(left_cell)
        self.datiCenter(center_cell)
        self.datiRight(right_cell)

    def datiLeft(self, c):
        l = c.layout('dati_left',
                    lbl_class='cell_label',
                    border_width=0)
                
        r = l.row(height=8)
        r.cell(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.nome'), lbl='Name of ship')
        r = l.row(height=8)
        r.cell(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.@flag.nome'), lbl='Flag of ship')
    def datiCenter(self, c):
        l = c.layout('dati_center',
                    lbl_class='cell_label',
                    border_width=0)

        r = l.row(height=8)
        r.cell(self.field('@arrival_id.voy_n'), lbl='Voyage no.')
        r = l.row(height=8)
        r.cell(self.field('@arrival_id.@agency_id.@port.citta_nazione'), lbl='Port of loading')

    def datiRight(self, c):
        l = c.layout('dati_right',
                     lbl_class='cell_label',
                     border_width=0)
        l.row(height=8).cell(self.field('freight'), lbl='Freight')
        l.row(height=8).cell(self.field('destination'), lbl='Place of destination')
        l.row(height=8).cell(self.field('departure'), lbl='Departure date')

    def defineCustomStyles(self):
        self.body.style(""".cell_label{
                            font-size:8pt;
                            text-align:left;
                            color:gray;
                            text-indent:1mm;}

                            .footer_content{
                            text-align:right;
                            margin:2mm;
                            }
                            """)


    def gridStruct(self,struct):
        r = struct.view().rows()
        r.fieldcell('bl_n',mm_width=10, name='B/L no.', subtotal='Total BL no. {breaker_value}')
        r.fieldcell('scn', content_class="breakword", name='(S) Shipper (C) Consigne (N) Notify')
        r.fieldcell('marks_n',mm_width=30, name='Marks no.')
        r.fieldcell('pack_n',mm_width=10)
        r.fieldcell('descr_goods', content_class="breakword",mm_width=60)
        r.fieldcell('measure_id',mm_width=10, name='Measure')
        r.fieldcell('qt_bl',mm_width=20, totalize=True,format='#,###.000')
        r.fieldcell('remarks', mm_width=40)

    def gridQueryParameters(self):
        return dict(relation='@bl_cargodocs')
        #Nel metodo gridQueryParameters è possibile anche utilizzare le relazioni

    def calcRowHeight(self):
        #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
        scn_offset = 65
        descr_goods_offset = 150
        #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
        #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
        #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
        n_rows_scn = len(self.rowField('scn'))//scn_offset
        n_rows_descr = len(self.rowField('descr_goods'))//descr_goods_offset + 1.2
        n_rows = max(n_rows_scn,n_rows_descr)#, n_rows_nome_provincia)
        height = (self.grid_row_height * n_rows)
        return height

    def docFooter(self, footer, lastPage=None):
        l = footer.layout('totali_fattura',top=1,
                           lbl_class='cell_label', 
                           content_class = 'footer_content')
        #r = l.row(height=5)
        #r.cell()
        #r.cell(self.field('totale_imponibile'),lbl='Imponibile',  width=20)
        #r.cell(self.field('totale_iva'),lbl='IVA',  width=20)
        #r.cell(self.field('totale_fattura'),lbl='Totale',  width=20)
