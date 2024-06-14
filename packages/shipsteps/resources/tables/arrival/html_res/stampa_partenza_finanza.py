#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-
#
#  Stampa Partenza Finanza


from gnr.web.gnrbaseclasses import TableScriptToHtml
import datetime

class Main(TableScriptToHtml):
    maintable = 'shipsteps.arrival'
    virtual_columns = '$gdf_int,@agency_id.fullstyle,$nextport'
    #Con virtual_columns aggiungo a self.record anche le formulaColumn calcolate che altrimenti di default non verrebbero compilate 
    
    def main(self):
        self.schedaCliente()
        #Nel metodo main specifichiamo tutti i metodi da eseguire: in questo caso solo un metodo schedaCliente totalmente customizzato

    def schedaCliente(self):
        self.paperpage = self.getNewPage()
        layout = self.paperpage.layout(
                            um='mm',top=10,left=14,right=4, bottom=3,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='9pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='grey')

       # layout.row(height=10).cell("<div style='font-size:20pt;padding:5px'><strong>Dati Anagrafici</strong></div>::HTML")
        dati_agenzia = layout.row(height=40, lbl_height=2, lbl_class='smallCaption')
        layout.row(height=10).cell()
        dati_finanza = layout.row(height=40, lbl_height=4, lbl_class='smallCaption')
        layout.row(height=10).cell("<div style='font-size:14pt;padding:5px'><strong>PARTENZA DELLA NAVE</strong></div>::HTML")
        griglia_nave = layout.row(height=74, lbl_height=4, lbl_class='smallCaption')
        dati_firma = layout.row(height=40, lbl_height=4, lbl_class='smallCaption')
        self.datiAgenzia(dati_agenzia)
        self.datiFinanza(dati_finanza)
        self.datiNave(griglia_nave)
        self.datiFirma(dati_firma)
     
    def datiAgenzia(self, row):
       # agenzia = self.field('@agency_id.agency_name'), font_size='14pt'
        indirizzo = (self.field('@agency_id.description') + '<br>' + self.field('@agency_id.address') + '<br>Tel.: ' + self.field('@agency_id.tel') + '<br>Fax:' +
                    self.field('@agency_id.fax') + '<br>' + self.field('@agency_id.email') + '<br>' + self.field('@agency_id.web') + '::HTML')
        #print(X)
        dati_layout = row.cell().layout(name='datiAgenzia', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        dati_layout.row(height=8).cell(self.field('@agency_id.agency_name'), font_size='14pt',font_weight= 'bold')                            
        dati_layout.row().cell(indirizzo)
       # dati_layout.row().cell(indirizzo, lbl="Indirizzo")
        #aggiungo una colonna a destra
        contatti_layout = row.cell().layout()
        #contatti_layout = row.cell().layout(name='contattiCliente', um='mm', border_color='grey', lbl_class='smallCaption',
        #                            lbl_height=3, style='line-height:5mm;text-indent:2mm;')
      #  contatti_layout.row().cell(self.field('email'), lbl="Email")
      #  contatti_layout.row().cell(self.field('iscritto_newsletter'), lbl="Iscritto newsletter")

    def datiFinanza(self, row):
        #aggiungo una colonna a destra
        contatti_layout = row.cell().layout()
        dati_layout = row.cell().layout(name='datiCliente', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        finanza = 'Spett.<br>' + self.field('gdf_int') + '::HTML'
        #dati_layout.row(height=5).cell('Spett.',font_weight= 'bold')
        dati_layout.row().cell(finanza,font_weight= 'bold', font_size='14pt')
        
      # fatture_layout = row.cell().layout(name='datiFatture', um='mm', border_color='grey', lbl_class='smallCaption',
      #                             lbl_height=3, style='line-height:5mm;text-indent:2mm;')
      # 
      # fatture_layout.row(height=8).cell("Elenco delle fatture emesse al cliente dal momento dell'acquisizione a oggi")

      # intestazione = fatture_layout.row(height=6)
      # intestazione.cell("Estremi documento", content_class='aligned_center')
      # intestazione.cell("Imponibile", content_class='aligned_center')

      # fatture = self.record['@fatture']
      # for f in fatture.values():
      #     estremi_documento = "Fattura num. {protocollo} del {data}".format(protocollo=f['protocollo'], data=f['data'])
      #     r = fatture_layout.row(height=5)
      #     r.cell(estremi_documento)
      #     r.cell(self.toText(f['totale_imponibile'], format=self.currencyFormat), content_class='aligned_right')

      # fatture_layout.row().cell()
      # footer_fatture = fatture_layout.row(height=10)
      # footer_fatture.cell(self.record['n_fatture'], lbl="Num. Fatture", content_class='aligned_right')
      # footer_fatture.cell(self.toText(self.record['tot_fatturato'], format=self.currencyFormat), lbl="Tot. Fatturato", content_class='aligned_right')
    
    def datiNave(self, row):
        nave = ('<br>' + self.field('@vessel_details_id.@imbarcazione_id.tip_imbarcazione_code') + ' ' + self.field('@vessel_details_id.@imbarcazione_id.nome') +
                ' di bandiera ' + self.field('@vessel_details_id.@imbarcazione_id.bandiera') + '::HTML')
        dati_layout = row.cell().layout(name='datiNave', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        dati_layout.row(height=10).cell(nave,font_weight= 'bold', font_size='14pt')
        dati_layout.row(height=10).cell('<br>Destinazione: ' + self.field('nextport') + '::HTML', font_size='14pt')
        dati_layout.row(height=10).cell('<br>Partenza: ' + self.field('@time_arr.sailed') + '::HTML', font_size='14pt')
        carico=str(self.parameter('carico_partenza'))
        if carico == 'None':
            carico = 'VUOTA'    
        dati_layout.row(height=10).cell('<br>Carico: ' + carico + '::HTML', font_size='14pt')
        data_att = self.parameter('data_att').strftime("%d/%m/%Y")
        dati_layout.row().cell('<br><br><br>' + str(self.field('@agency_id.@port.descrizione')) + ' ' + '{data}'.format(data=data_att) + '::HTML', font_size='14pt')
        
    
    def datiFirma(self, row):
        datifirma=row.cell().layout()
        dati_layout = row.cell().layout(name='datiNave', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        
        dati_layout.row().cell(self.field('@agency_id.agency_name'), font_size='14pt')
       # prodottiLayout = row.cell().layout(name='datiProdotti', um='mm', border_color='grey', lbl_class='smallCaption',
       #                             lbl_height=3, style='line-height:5mm;text-indent:2mm;')
    #
       # prodottiLayout.row(height=8).cell("Elenco dei 10 prodotti più venduti al cliente ordinati per fatturato totale, dal momento dell'acquisizione a oggi")
#
       # intestazione = prodottiLayout.row(height=6)
       # intestazione.cell("Prodotto", width=0, content_class='aligned_center')
       # intestazione.cell("Quantità", width=30, content_class='aligned_center')
       # intestazione.cell("Tot.Fatturato", width=30, content_class='aligned_center')
#
       # prodotti = self.db.table('fatt.fattura_riga').query(columns="""$cliente_id,
       #                                             @prodotto_id.descrizione AS prodotto, 
       #                                             SUM($quantita) AS quantita, 
       #                                             SUM($prezzo_totale) AS prezzo_totale""",
       #                                             where = '$cliente_id=:cliente',
       #                                             cliente=self.record['id'],
       #                                             group_by='$cliente_id,@prodotto_id.descrizione',
       #                                             order_by='SUM($prezzo_totale) DESC',
       #                                             limit=10).fetch()
       #                                             #Raggruppiamo righe risultato della query per prodotto
#
       # for p in prodotti:
       #     r = prodottiLayout.row(height=6)
       #     r.cell(p['prodotto'], width=0)
       #     r.cell(p['quantita'], width=30, content_class='aligned_right')
       #     r.cell(self.toText(p['prezzo_totale'], format=self.currencyFormat), width=30, content_class='aligned_right')
#
    def outputDocName(self, ext=''):
        return 'Partenza_gdf.{ext}'.format(ext=ext)

        #return 'Scheda cliente_{cliente}.{ext}'.format(cliente=self.record['reference_num'], ext=ext)
