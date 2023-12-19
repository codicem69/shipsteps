from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime

class Main(TableScriptToHtml):
    maintable= 'shipsteps.shorepass'
    #row_table = 'shipsteps.shorepass'
    page_width = 297
    page_height = 210
    page_margin_left = 5
    page_margin_right = 5
    doc_header_height = 30
    doc_footer_height = 50
    grid_header_height = 20
    css_requires='grid'
    #totalize_footer='Totale'
    #Fornendo a totalize_footer una stringa testuale, questa verrà usata come etichetta della riga di totalizzazione
    empty_row=dict()
    #Grazie a questo parametro in caso di mancanza di dati verrà stampata una griglia vuota invece di una pagina bianca
    virtual_columns = '@arrival_id.@vessel_details_id.@imbarcazione_id.@flag.codename,@arrival_id.lastport' #aggiungiamo le colonne calcolate
    
    def docHeader(self, header):
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()
        crewlist = self.record['arr_dep']
        row.cell("""<center><div style='font-size:12pt;'><strong>{crew_type} CREW LIST</strong></div>
                    </center>::HTML""".format(crew_type=crewlist))
        layout = header.layout(
                            um='mm',top=10,left=1,right=1, bottom=3,
                            border_width=0.2,
                            font_family='Helvetica',
                            font_size='8pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='grey')
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        
        dati_crewlist = layout.row(height=16, lbl_height=2, lbl_class='smallCaption')
        #layout.row(height=2).cell()
        #row_cell = row.cell()
        self.datiCrewlist(dati_crewlist)
      

    
    def datiCrewlist(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='grey', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;',vertical_align= 'middle',content_class='aligned_center')
        cel1=col1.row(height=8).cell(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.nome'), font_size='10pt',font_weight= 'bold', lbl='Name of ship')
        col2=cel1.row.cell().layout(name='col2', um='mm', border_color='grey',row_border=False, lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='aligned_center')
        col2.row(height=8).cell(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.imo'), font_size='10pt',font_weight= 'bold', lbl='IMO No.')
        col3=cel1.row.cell().layout(name='col3', um='mm', border_color='grey',row_border=False, lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='aligned_center')
        col3.row(height=8).cell(self.field('@arrival_id.@vessel_details_id.callsign'), font_size='10pt',font_weight= 'bold', lbl='Call sign')
        col4=cel1.row.cell().layout(name='col4', um='mm', border_color='grey',row_border=False, lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='aligned_center')
        col4.row(height=8).cell(self.field('@arrival_id.voy_n'), font_size='10pt',font_weight= 'bold', lbl='Voyage number')
        cel2=col1.row(height=8).cell(self.field('@arrival_id.@agency_id.@port.citta_nazione'), font_size='10pt',font_weight= 'bold', lbl='Port of arrival / departure')
        col2_2=cel2.row.cell().layout(name='col2_2', um='mm', border_color='grey',row_border=False, lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='aligned_center')
        col2_2.row(height=8).cell(self.field('data_arr'), font_size='10pt',font_weight= 'bold', lbl='Date of Arrival/Departure')
        col3_2=cel2.row.cell().layout(name='col3_2', um='mm', border_color='grey',row_border=False, lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='aligned_center')
        col3_2.row(height=8).cell(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.@flag.codename'), font_size='10pt',font_weight= 'bold', lbl='Flag state of ship')
        col4_2=cel2.row.cell().layout(name='col4_2', um='mm', border_color='grey',row_border=False, lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='aligned_center')
        col4_2.row(height=8).cell(self.field('@arrival_id.lastport'), font_size='10pt',font_weight= 'bold', lbl='Last port of call')

    def defineCustomStyles(self):
        #Questo metodo definisce gli stili del body dell'html
        self.body.style(""".cell_label{
                            font-size:8pt;
                            text-align:left;
                            color:grey;
                            text-indent:1mm;}

                            .footer_content{
                            text-align:right;
                            margin:2mm;
                            font-size:8pt;
                            }
                            """)

    def gridStruct(self,struct):
        #Questo metodo definisce la struttura della griglia di stampa definendone colonne e layout
        r = struct.view().rows()
        r.fieldcell('_row_count',mm_width=5, content_class="breakword",name='no.')
        r.fieldcell('name', mm_width=0, name="""<div>Given name<br>Nome</div>::HTML""", content_class="breakword")
        #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
        #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.fieldcell('surname', mm_width=0, name="""<div>Family Name<br>Cognome</div>::HTML""", content_class="breakword")
        #r.fieldcell('cliente_id', mm_width=0)
        r.fieldcell('rank',mm_width=0, name="""<div>Rank or rating<br>Ruolo</div>::HTML""", content_class="breakword")
        r.fieldcell('nationality', mm_width=0, name="""<div>Nationality<br>Nazionalità</div>::HTML""", content_class="breakword")
        r.fieldcell('birth_date', mm_width=16, name="""<div>Date of birth<br>Data di nascita</div>::HTML""", content_class="breakword")
        r.fieldcell('birth_place', mm_width=0, name="""<div>Place of birth<br>Luogo di nascita</div>::HTML""", content_class="breakword")
        r.fieldcell('birth_country',mm_width=0, name="""<div>Country of birth<br>Stato di nascita</div>::HTML""", content_class="breakword")
        r.fieldcell('gender',mm_width=10, name="""<div>Gender<br>Sesso</div>::HTML""", content_class="breakword")
        r.fieldcell('id_doc',mm_width=15, name="""<div>Nature of identity document<br>Tipo di documento</div>::HTML""", content_class="breakword")
        r.fieldcell('id_doc_n',mm_width=20, name="""<div>Number of identity document<br>Numero del documento di identità</div>::HTML""", content_class="breakword")
        r.fieldcell('id_doc_state',mm_width=0, name="""<div>Issuing State of identity document<br>Stato di rilascio del documento di identità</div>::HTML""", content_class="breakword")
        r.fieldcell('expire_id_doc',mm_width=20, name="""<div>Expiry date of identity document<br>Data di scadenza del documento di identità</div>::HTML""", content_class="breakword")

    def gridQueryParameters(self):
        return dict(relation='@shorepass_righe')
        #Nel metodo gridQueryParameters è possibile anche utilizzare le relazioni

    def calcRowHeight(self):
        #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
        doc_offset = 10
        #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
        #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
        #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
        n_rows_name = len(self.rowField('name'))//doc_offset
        n_rows_surname = len(self.rowField('surname'))//doc_offset
        n_rows_rank = len(self.rowField('rank'))//12
        n_rows_nationality = len(self.rowField('_nationality_codename'))//20 + 1
        n_rows_birthcountry = len(self.rowField('_birth_country_codename'))//20 + 1
        n_rows_docstate = len(self.rowField('_id_doc_state_codename'))//20 + 1
        n_rows_docn = len(self.rowField('id_doc_n'))//12 + 1
        
        #In caso di valori in relazione, è necessario utilizzare "_" nel metodo rowField per recuperare correttamente i valori
        #A tal proposito si consiglia comunque sempre di utilizzare le aliasColumns
        n_rows = max(n_rows_name,n_rows_surname,n_rows_rank,n_rows_nationality,n_rows_birthcountry,n_rows_docstate,n_rows_docn)#, n_rows_nome_provincia)
        #print(x)
        height = (self.grid_row_height * n_rows)
        return height
    
    def docFooter(self, footer, lastPage=None):
        
        layout = footer.layout(
                            um='mm',top=1,left=1,right=1, bottom=10,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='8pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='white')
        dati_firma = layout.row(height=5, lbl_height=2, lbl_class='smallCaption')
 
        self.datiFirma(dati_firma)
      
    def datiFirma(self, row):
        firma = row.cell().layout(name='firma', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        stamp=self.field('@arrival_id.vessel_stamp')
        firma.row(height=0).cell("""<img src="%s" width="auto" height="200">::HTML""" %stamp,width=0,content_class='aligned_center')
         
    def outputDocName(self, ext=''):
        #Questo metodo definisce il nome del file di output
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        nome_imb='_'.join(self.field('@arrival_id.@vessel_details_id.@imbarcazione_id.nome').split(' '))
        doc_name = 'Crew_list_{nave}{ext}'.format(nave=nome_imb, ext=ext)
        return doc_name
