#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-
#
#  Stampa Partenza Finanza

from gnr.web.gnrbaseclasses import TableScriptToHtml
import datetime

class Main(TableScriptToHtml):

    row_table = 'shipsteps.shipdoc_pmis'
    page_width = 210
    page_height = 297
    page_margin_left = 5
    page_margin_right = 5
    doc_header_height = 30
    doc_footer_height = 8
    grid_header_height = 5
    grid_row_height = 7
    empty_row=dict()
    css_requires='grid'
    #Grazie a questo parametro in caso di mancanza di dati verrà  stampata una griglia vuota invece di una pagina bianca

    def gridLayoutParameters(self):
        # FIX CHIAVE: top=0, bottom=0 per non ridurre la larghezza utile calcolata
        # in structAnalyze (copyWidth - layout margins). Con i valori default 0.1
        # la somma colonne (287mm) supera la larghezza utile percepita dal framework
        # e scatta il multi-sheet che spezza le righe.
        # Aggiungiamo anche overflow:hidden sul contenitore griglia così le righe
        # in eccesso non sfondano sul footer.
        return dict(name='gridLayout', um='mm', border_color='#e0e0e0',
                    top=0, bottom=0, left=0, right=0,
                    font_size='12pt',
                    border_width=0.3, lbl_class='caption',
                    text_align='left',
                    cell_height=10,
                    overflow='hidden')

    def docHeader(self, header):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()
        row.cell("<div style='font-size:16pt;padding:2px;text-align: center'><strong>LISTA CERTIFICATI DA INSERIRE NEL PMIS</strong></div>::HTML")

        
    
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
                            }
                            """)

    def gridStruct(self,struct):
        #Questo metodo definisce la struttura della griglia di stampa definendone colonne e layout
        r = struct.view().rows()
        r.fieldcell('description', content_class="breakword_font")
        #r.fieldcell('totale_fattura', mm_width=20, totalize=True)

    def gridQueryParameters(self):
        #Questo metodo fornisce a gridData i parametri (condizioni, relation, table) sulla base dei quali costruire
        #le righe con i dati da riportare in griglia. In questo caso uso una condizione.
        condition=['']
        return dict(condition=' AND '.join(condition))

    def docFooter(self, footer, lastPage=None):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        foo = footer.layout('totali_doc',top=1,
                           lbl_class='cell_label',
                           content_class = 'footer_content')
        r = foo.row()
        #r.cell('Documento stampato il {oggi}'.format(oggi=self.db.workdate))

    def outputDocName(self, ext=''):
        #Questo metodo definisce il nome del file di output
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
            doc_name = 'Lista_doc_PMIS_{ext}'.format(ext=ext)
        return doc_name
