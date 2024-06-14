#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-
#
#  Stampa Partenza Finanza

from gnr.web.gnrbaseclasses import TableScriptToHtml
import datetime

class Main(TableScriptToHtml):
    maintable = 'shipsteps.arrival'
    virtual_columns = '$cp_int,@agency_id.fullstyle, $workport,@vessel_details_id.@imbarcazione_id.@flag.codename'
    #Con virtual_columns aggiungo a self.record anche le formulaColumn calcolate che altrimenti di default non verrebbero compilate 
    
    def main(self):
        self.schedaCliente()
        #Nel metodo main specifichiamo tutti i metodi da eseguire: in questo caso solo un metodo schedaCliente totalmente customizzato

    def schedaCliente(self):
        self.paperpage = self.getNewPage()
        layout = self.paperpage.layout(
                            um='mm',top=10,left=5,right=4, bottom=3,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='9pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='grey')

        #dati_agenzia = layout.row(height=40, lbl_height=2, lbl_class='smallCaption')
        layout.row(height=10).cell()
        dati_cp = layout.row(height=40, lbl_height=4, lbl_class='smallCaption')
        layout.row(height=10).cell("<div style='font-size:14pt;padding:0px'><strong><center>DICHIARAZIONE DISPONIBILITÀ FONDI</center></strong></div>::HTML")
        griglia_doc = layout.row(height=120, lbl_height=4, lbl_class='smallCaption')
        dati_firma = layout.row(height=60, lbl_height=4, lbl_class='smallCaption')
        #self.datiAgenzia(dati_agenzia)
        self.datiCapitaneria(dati_cp)
        self.datiDoc(griglia_doc)
        self.datiFirma(dati_firma)
     
    def datiAgenzia(self, row):
        indirizzo = (self.field('@agency_id.description') + '<br>' + self.field('@agency_id.address') + '<br>Tel.: ' + self.field('@agency_id.tel') + '<br>Fax:' +
                    self.field('@agency_id.fax') + '<br>' + self.field('@agency_id.email') + '<br>' + self.field('@agency_id.web') + '::HTML')
        dati_layout = row.cell().layout(name='datiAgenzia', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        dati_layout.row(height=8).cell(self.field('@agency_id.agency_name'), font_size='14pt',font_weight= 'bold')                            
        dati_layout.row().cell(indirizzo)
        contatti_layout = row.cell().layout()


    def datiCapitaneria(self, row):
        #aggiungo una colonna a destra
        contatti_layout = row.cell().layout()
        dati_layout = row.cell().layout(name='datiCliente', um='mm', border_color='white', lbl_class='smallCaption',margin_right='20px',
                                    lbl_height=3, style='line-height:5mm;')
        cp = 'Spett.<br>' + self.field('cp_int') + '::HTML'
        #dati_layout.row(height=5).cell('Spett.',font_weight= 'bold')
        dati_layout.row().cell(cp,font_weight= 'bold', font_size='14pt')
        
    
    def datiDoc(self, row):
        dati_agent = ('<br>' + "Il sottoscritto " + self.field('@agency_id.agent_name') + " iscritto al N° " + self.field('@agency_id.cciaa_n') + " dell'elenco dei Raccomandatari Marittimi presso la CIAA di "
                      + self.field('@agency_id.cciaa_place') + ", operante nel porto di " + self.field('workport') + " come Raccomandatario Marittimo del/lla:" + '::HTML')
        nave = (self.field('@vessel_details_id.@imbarcazione_id.tip_imbarcazione_code') + ' ' + self.field('@vessel_details_id.@imbarcazione_id.nome') + '::HTML')
        dati_layout = row.cell().layout(name='datiDoc', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        dati_layout.row().cell(dati_agent, font_size='14pt')
        dati_layout.row(height=10).cell(nave,font_weight= 'bold', font_size='14pt', content_class = 'aligned_center')
        dati_layout.row(height=10).cell('Bandiera: '+self.field('@vessel_details_id.@imbarcazione_id.@flag.codename'),font_weight= 'bold', font_size='14pt')
        dati_layout.row(height=10).cell('IMO n.: ' + self.field('@vessel_details_id.@imbarcazione_id.imo'),font_weight= 'bold', font_size='14pt')
        dati_layout.row().cell("""Dichiara  ai  sensi  dell’Art.3  della  Legge  4.4. 1977  N°  135  di  avere la disponibilità nel territorio Italiano 
                               della somma in valuta sufficiente a garantire l'adempimento delle obbligazioni assunte suo tramite in occasione dell'approdo 
                               della nave citata nel porto di """ + self.field('workport') + '::HTML', font_size='14pt')
        dati_layout.row(height=10).cell('Cogliamo l’occasione per porgere i nostri più cordiali saluti.' + '::HTML', font_size='14pt')
        #data_att = self.parameter('data_att').strftime("%d/%m/%Y")
        data_att = self.db.workdate.strftime("%d/%m/%Y")
        dati_layout.row().cell(str(self.field('@agency_id.@port.descrizione')) + ' ' + '{data}'.format(data=data_att) + '::HTML', font_size='14pt')
        
    
    def datiFirma(self, row):
        datifirma=row.cell().layout()
        dati_layout = row.cell().layout(name='datiNave', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        dati_layout.row(height=10).cell(self.field('@agency_id.agency_name'), font_size='14pt')
        timbro=self.record['@agency_id.agency_stamp']
        dati_layout.row().cell("""<img src="%s" height="100">::HTML""" %timbro)
        dati_layout.row().cell('')

    def outputDocName(self, ext=''):
        nave=self.record['@vessel_details_id.@imbarcazione_id.nome']
        return 'Disp_valuta_{nave}.{ext}'.format(nave=nave,ext=ext)

        #return 'Scheda cliente_{cliente}.{ext}'.format(cliente=self.record['reference_num'], ext=ext)
