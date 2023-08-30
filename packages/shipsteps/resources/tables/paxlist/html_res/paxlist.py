from gnr.web.gnrbaseclasses import TableScriptToHtml
from gnr.core.gnrbag import Bag
from gnr.core.gnrdecorator import public_method

class Main(TableScriptToHtml):
    #pdf_service = 'wk'
    maintable = 'shipsteps.paxlist'
    #Non indicheremo una row_table ma solo una maintable perché stamperemo i record della selezione corrente
    virtual_columns = '@arrival_id.workport,@arrival_id.@vessel_details_id.@imbarcazione_id.@flag.codename,@arrival_id.lastport'
    css_requires='grid'

    doc_header_height = 33
    doc_footer_height = 20
    grid_header_height = 12
    grid_row_height = 5
    

    def defineCustomStyles(self):
        self.body.style(""".cell_label{
                            font-size 8pt;
                            text-align:left;
                            color:gray;
                            text-indent:0.5mm;
                            width:auto;
                            font-weight: normal;
                            #line-height:auto;
                            line-height:3mm;
                            height:3mm;}
    
                            .footer_content{   
                            text-align:right;
                            margin:2mm;
                            }
                            """)


    def docHeader(self, header):
        layout = header.layout(name='doc_header', margin='0mm', border_width=0,top=0.1,left=0.1)
        r = layout.row(row_border=False,height=5)
        
        if self.record['arr_dep'] == 'True':
            paxlist = 'Arrival / Arrivo'
        else:
            paxlist = 'Departure / Partenza'
 
        r.cell("""<center><div style='font-size:12pt;'><strong>PASSENGER LIST</strong></div>
                    <div style='font-size:12pt;'> {pax_type}</div></center>::HTML""".format(pax_type=paxlist))
        layout = header.layout(name='doc_header', margin='0mm', border_width=0.5,top=12,left=0.1)
        
        r = layout.row(height=5)
        r.cell('Name of Ship / Nome della Nave',content_class='aligned_center', font_size='10pt', width=72)
        r.cell('IMO no.',content_class='aligned_center', font_size='10pt', width=70)
        r.cell('Call Sign / Nominativo internazionale',content_class='aligned_center', font_size='10pt', width=70)
        r.cell('Voyage no. / N. viaggio',content_class='aligned_center', font_size='10pt', width=70)
        r = layout.row(height=5)
        r.cell(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.nome'),width=72,content_class='aligned_center',font_weight='bold', font_size='10pt') 
        r.cell(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.imo'),width=70,content_class='aligned_center',font_weight='bold', font_size='10pt') 
        r.cell(self.field('@arrival_id.@vessel_details_id.callsign'),width=70,content_class='aligned_center',font_weight='bold', font_size='10pt') 
        r.cell(self.field('@arrival_id.voy_n'),width=70,content_class='aligned_center',font_weight='bold', font_size='10pt') 
        r = layout.row(height=5)
        r.cell('Port of Arrival / Departure - Porto di Arrivo / Partenza',content_class='aligned_center', font_size='10pt', width=72)
        r.cell('Date of Arrival / Departure - Data di Arrivo / Partenza ',content_class='aligned_center', font_size='10pt', width=70)
        r.cell('Flag state of ship - Bandiera',content_class='aligned_center', font_size='10pt', width=70)
        r.cell('Last port of call - Ultimo porto toccato',content_class='aligned_center', font_size='10pt', width=70)
        r = layout.row(height=5)
        r.cell(self.field('@arrival_id.workport'),width=72,content_class='aligned_center',font_weight='bold', font_size='10pt') 
        r.cell(self.field('@arrival_id.etb'),width=70,content_class='aligned_center',font_weight='bold', font_size='10pt') 
        r.cell(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.@flag.codename'),width=70,content_class='aligned_center',font_weight='bold', font_size='10pt') 
        r.cell(self.field('@arrival_id.lastport'),width=70,content_class='aligned_center',font_weight='bold', font_size='10pt') 
     

    def gridStruct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count',mm_width=5, content_class="breakword",name='no.')
        r.fieldcell('name',mm_width=0, content_class="breakword")
        r.fieldcell('surname',mm_width=0, content_class="breakword")
        r.fieldcell('nationality',mm_width=0, content_class="breakword")
        r.fieldcell('birth_date',mm_width=0, content_class="breakword")
        r.fieldcell('birth_place',mm_width=0, content_class="breakword")
        r.fieldcell('birth_country',mm_width=0, content_class="breakword")
        r.fieldcell('gender',mm_width=0, content_class="breakword")
        r.fieldcell('id_doc',mm_width=0, content_class="breakword")
        r.fieldcell('id_doc_n',mm_width=17, content_class="breakword")
        r.fieldcell('id_doc_state',mm_width=0, content_class="breakword", name='Issuing State of identity or travel document')
        r.fieldcell('expire_id_doc',mm_width=0, content_class="breakword")
        r.fieldcell('port_embark',mm_width=0, content_class="breakword")
        r.fieldcell('port_disembark',mm_width=0, content_class="breakword")
        r.fieldcell('transit',mm_width=11, content_class="breakword")
        r.fieldcell('visa_n',mm_width=0, content_class="breakword", name='Visa number if appropriate')
        
    def gridQueryParameters(self):
        return dict(relation='@paxlist_righe')
        #Nel metodo gridQueryParameters è possibile anche utilizzare le relazioni

    
    def calcRowHeight(self):
        #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
        nationality_offset = 15
        doc_offset = 10
        #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
        #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
        #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
        n_rows_name = len(self.rowField('name'))//doc_offset + 1
        n_rows_surname = len(self.rowField('surname'))//doc_offset + 1
        n_rows_nationality = len(self.rowField('_nationality_codename'))//nationality_offset + 1
        n_rows_birthcountry = len(self.rowField('_birth_country_codename'))//nationality_offset + 1
        n_rows_docstate = len(self.rowField('_id_doc_state_codename'))//nationality_offset + 1
        n_rows_docn = len(self.rowField('id_doc_n'))//doc_offset + 1
        n_rows_portembark = len(self.rowField('port_embark'))//doc_offset + 1
        n_rows_portdisembark = len(self.rowField('port_disembark'))//doc_offset + 1
        #In caso di valori in relazione, è necessario utilizzare "_" nel metodo rowField per recuperare correttamente i valori
        #A tal proposito si consiglia comunque sempre di utilizzare le aliasColumns
        n_rows = max(n_rows_name,n_rows_surname,n_rows_nationality,n_rows_birthcountry,n_rows_docstate,n_rows_docn,n_rows_portembark,n_rows_portdisembark )#, n_rows_nome_provincia)
        #print(x)
        height = (self.grid_row_height * n_rows)
        return height

    def docFooter(self, footer, lastPage=None):
        
        l = footer.layout('footer',top=0,left=0.1, border_width=0,
                           lbl_class='caption', 
                           content_class = 'footer_content')
        
        r = l.row(row_border=False,height=5)
        timbro=self.record['@arrival_id.vessel_stamp']
        r.cell("""<img src="%s" width="auto" height="80">::HTML""" %timbro,width=0)

    def calcDocFooterHeight(self):  
            if self.record['noteproforma']:
            
                return self.doc_header_height + 50
            else:
                return self.doc_footer_height    

        
