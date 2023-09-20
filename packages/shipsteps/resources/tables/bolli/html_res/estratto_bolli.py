from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime

class Main(TableScriptToHtml):
    maintable = 'shipsteps.bolli'
    row_table = 'shipsteps.bolli'
    page_width = 297
    page_height = 210
    page_margin_left = 5
    page_margin_right = 5
    doc_header_height = 30
    doc_footer_height = 15
    grid_header_height = 10
    totalize_footer='Totale'
    #Fornendo a totalize_footer una stringa testuale, questa verrà usata come etichetta della riga di totalizzazione
    empty_row=dict()
    #Grazie a questo parametro in caso di mancanza di dati verrà stampata una griglia vuota invece di una pagina bianca
    virtual_columns = '$tot_tr14,$tot_tr22,$nome_agenzia' #aggiungiamo le colonne calcolate

    def docHeader(self, header):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()

        if self.parameter('anno'):
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto Bolli <br>{anno}</strong></div>
                     <div style='font-size:14pt;'><strong>{agenzia}</strong></div></center>::HTML""".format(anno=self.parameter('anno'),agenzia=self.rowField('nome_agenzia')))
        #print(x)
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
        #r.fieldcell('@cliente_id.rag_sociale', mm_width=62, subtotal='Totale documento {breaker_value}',subtotal_order_by='@cliente_id.rag_sociale,$data,$doc_n')
        r.fieldcell('date', mm_width=25)
        #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
        #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.fieldcell('imbarcazione_id', mm_width=50, name='Imbarcazione')
        #r.fieldcell('cliente_id', mm_width=0)
        r.fieldcell('istanza',mm_width=0, name='Descrizione')
        r.fieldcell('note',mm_width=0)
        r.fieldcell('nome_agenzia',mm_width=0)
        r.fieldcell('bolli_tr14', mm_width=20,name="""<center><div><strong>Bolli € 16,00 <br>tributo 14</strong></div>
                    </center>::HTML""", totalize=True)
        r.fieldcell('bolli_tr22', mm_width=20, name="""<center><div><strong>Bolli € 16,00 <br>tributo 22</strong></div>
                    </center>::HTML""", totalize=True)
        
    def gridQueryParameters(self):
        
        condition=[]
        balance=0

        if self.parameter('anno'):
            condition.append('$anno_doc=:anno')

        result = dict(table='shipsteps.bolli',condition=' AND '.join(condition), condition_anno=self.parameter('anno'),order_by='$date ASC')#,relation='@fatt_cliente')
        #print(x)
        return result

    def docFooter(self, footer, lastPage=None):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        foo = footer.layout('totale_bolli',top=1,
                           lbl_class='cell_label', 
                           content_class = 'footer_content',border_color='white')
        r = foo.row()
        today = self.db.workdate.strftime("%d/%m/%Y")
        r.cell('Document printed on {oggi}'.format(oggi=today))

    def outputDocName(self, ext=''):
        #Questo metodo definisce il nome del file di output
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        if self.parameter('anno'):
            doc_name = 'Estratto_bolli_{anno}_{ext}'.format(anno=self.parameter('anno'), ext=ext)
        else: 
            doc_name = 'Estratto_bolli_{ext}'.format(ext=ext)
        return doc_name
