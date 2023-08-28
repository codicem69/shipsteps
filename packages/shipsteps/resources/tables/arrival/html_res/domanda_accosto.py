#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-
#
#  Stampa domanda di accosto CP


from turtle import width
from gnr.web.gnrbaseclasses import TableScriptToHtml
import datetime

class Main(TableScriptToHtml):
    maintable = 'shipsteps.arrival'
    virtual_columns = """$cp_int,@agency_id.fullstyle,$nextport,@vessel_details_id.@owner_id.own_fullname,$lastport,$nextport,@cargo_lu_arr.cargo_lu_en_ita,
                         $ship_or_rec,$caricoarrivo,$chrtrs"""
    #Con virtual_columns aggiungo a self.record anche le formulaColumn calcolate che altrimenti di default non verrebbero compilate 
    css_requires='accosto'
    def main(self):
        self.datiDomanda()
        #Nel metodo main specifichiamo tutti i metodi da eseguire: in questo caso solo un metodo schedaCliente totalmente customizzato

    def datiDomanda(self):
        self.paperpage = self.getNewPage()
        layout = self.paperpage.layout(
                            um='mm',top=5,left=6,right=6, bottom=3,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='9pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='black')
        

        carico = self.record['@cargo_lu_arr']
        h_car=len(carico)*5
       # layout.row(height=10).cell("<div style='font-size:20pt;padding:5px'><strong>Dati Anagrafici</strong></div>::HTML")
        dati_agenzia = layout.row(height=25, lbl_height=2, lbl_class='smallCaption')
        #layout.row(height=10).cell()
        dati_cp = layout.row(height=20, lbl_height=4, lbl_class='smallCaption')
        layout.row(height=7).cell("<div style='font-size:14pt;padding:5px;text-align: center'><strong>DOMANDA DI ACCOSTO</strong></div>::HTML")
        dati_mandato = layout.row(height=25, lbl_height=4, lbl_class='smallCaption')
        dati_nave = layout.row(height=40, lbl_height=4, lbl_class='smallCaption')
        dati_viaggio = layout.row(height=15, lbl_height=4, lbl_class='smallCaption')
        dati_operazioni = layout.row(height=40+h_car,lbl_height=4, lbl_class='smallCaption')
        #dati_operazioni2 = layout.row( height=25, lbl_height=4, lbl_class='smallCaption')
        dati_servizi= layout.row( height=15, lbl_height=4, lbl_class='smallCaption')
        dati_extra= layout.row( height=17, lbl_height=4, lbl_class='smallCaption')
        dati_firma = layout.row(height=20,lbl_height=4, lbl_class='smallCaption')
        
        self.datiAgenzia(dati_agenzia)
        self.datiCP(dati_cp)
        self.datiMandato(dati_mandato)
        self.datiNave(dati_nave)
        self.datiViaggio(dati_viaggio)
        self.datiOperazioni(dati_operazioni)
       # self.datiOperazioni2(dati_operazioni2)
        self.datiServizi(dati_servizi)
        self.datiExtra(dati_extra)
        self.datiFirma(dati_firma)
        
    def datiAgenzia(self, row):
       # agenzia = self.field('@agency_id.agency_name'), font_size='14pt'
        indirizzo = (self.field('@agency_id.address') + '<br>Tel.: ' + self.field('@agency_id.tel') + '<br>Fax:' +
                    self.field('@agency_id.fax') + '<br>' + self.field('@agency_id.email') + '<br>' + self.field('@agency_id.web') + '::HTML')
        #print(X)
        dati_layout = row.cell().layout(name='datiAgenzia', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        dati_layout.row(height=8).cell(self.field('@agency_id.agency_name'), font_size='16pt',font_weight= 'bold')                            
        dati_layout.row().cell(self.field('@agency_id.description'))
       # dati_layout.row().cell(indirizzo, lbl="Indirizzo")
        #aggiungo una colonna a destra
        contatti_layout = row.cell().layout(name='indirizzoAgenzia', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:2,5mm;')
        #contatti_layout = row.cell().layout()
        contatti_layout.row().cell(indirizzo,text_align='right')
        #contatti_layout = row.cell().layout(name='contattiCliente', um='mm', border_color='grey', lbl_class='smallCaption',
        #                            lbl_height=3, style='line-height:5mm;text-indent:2mm;')
      #  contatti_layout.row().cell(self.field('email'), lbl="Email")
      #  contatti_layout.row().cell(self.field('iscritto_newsletter'), lbl="Iscritto newsletter")

    def datiCP(self, row):
        #aggiungo una colonna a destra
        contatti_layout = row.cell().layout()
        dati_layout = row.cell().layout(name='datiCliente', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        finanza = 'Spett.<br>' + self.field('cp_int') + '<br>Sezione Tecnica - Nostromo' + '::HTML'
        #dati_layout.row(height=5).cell('Spett.',font_weight= 'bold')
        dati_layout.row().cell(finanza,font_weight= 'bold', font_size='12pt')
        
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
    
    def datiMandato(self, row):
        mandato = ("Il/la sottoscritto/a agente raccomandatario marittimo "+self.field('@agency_id.agent_name')+" nato/a a " + self.field('@agency_id.birthplace') + " domiciliato/a presso l'agenzia Marittima " + self.field('@agency_id.agency_name') + " tel. " + self.field('@agency_id.tel') + " cell. " + self.field('@agency_id.mobile_agent') + "<br>" + "<div style='text-align: center;'> premesso<br></div>" +
                   "di aver ricevuto mandato, ai sensi dell'art.3 Legge 04/04/1977 n.135 da: " + self.field('mandatory') +"<br>Armatore: "+self.field('@vessel_details_id.@owner_id.own_fullname')+ '::HTML' )
        dati_layout = row.cell().layout(name='datiMandato', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:2,5mm;')
        dati_layout.row(height=25).cell(mandato,font_size='9pt')
       

    def datiNave(self, row):
        prima_col = row.cell(width=20).layout(name='Nave', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=20)
        datinave= "<div style='text-align: center;text-decoration:underline;padding: 65px 0;'>DATI NAVE</div>" + '::HTML'
        prima_col.row(height=40).cell(datinave, font_weight='bold', background='lightgrey')
        seconda_col = row.cell(width=35).layout(name='descrNave', um='mm', border_color='black',lbl_class='smallCaption',hasBorderTop=True,
                                    hasBorderLeft=True,lbl_height=3, style='line-height:5mm;',width=35,content_class='cellheader')
        seconda_col.row(height=5).cell('TIPO(*) E NOME NAVE ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('ANNO ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('MMSI ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('GT ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('LUNGHEZZA ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('Pescaggio POPPA ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('NUMERO ELICHE  ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('N.ELICHE PRUA  ', font_weight='bold', background='lightgrey')

        nave = (self.field('@vessel_details_id.@imbarcazione_id.tipo') + ' ' + self.field('@vessel_details_id.@imbarcazione_id.nome') + '::HTML')
        terza_col = row.cell(width=50).layout(name='nomeNave', um='mm', border_color='black',hasBorderTop=True,
                                    lbl_height=3, style='line-height:5mm;padding-left: 5px;',width=50,content_class='celldata')
        terza_col.row(height=5).cell(nave,font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@vessel_details_id.built'),font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@vessel_details_id.mmsi'),font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@vessel_details_id.@imbarcazione_id.gt'),font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@vessel_details_id.@imbarcazione_id.loa'),font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('draft_aft_arr'),font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@vessel_details_id.n_eliche'),font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@vessel_details_id.n_eliche_prua'),font_size='9pt', font_weight='bold')

        quarta_col = row.cell(width=35).layout(name='Nave', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=35,content_class='cellheader')
        quarta_col.row(height=5).cell('BANDIERA ', font_weight='bold', background='lightgrey')
        quarta_col.row(height=5).cell('IMO ', font_weight='bold', background='lightgrey')
        quarta_col.row(height=5).cell('NOM.INT. ', font_weight='bold', background='lightgrey')
        quarta_col.row(height=5).cell('NT. ', font_weight='bold', background='lightgrey')
        quarta_col.row(height=5).cell('LARGHEZZA ', font_weight='bold', background='lightgrey')
        quarta_col.row(height=5).cell('Pescaggio PRUA ', font_weight='bold', background='lightgrey')
        quarta_col.row(height=5).cell('N.ELICHE POPPA ', font_weight='bold', background='lightgrey')


        quinta_col = row.cell().layout(name='Nave', um='mm', border_color='black', lbl_class='',hasBorderTop=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='celldata')
        quinta_col.row(height=5).cell(self.field('@vessel_details_id.@imbarcazione_id.bandiera'),font_size='9pt', font_weight='bold')
        quinta_col.row(height=5).cell(self.field('@vessel_details_id.@imbarcazione_id.imo'),font_size='9pt', font_weight='bold')
        quinta_col.row(height=5).cell(self.field('@vessel_details_id.callsign'),font_size='9pt', font_weight='bold')
        quinta_col.row(height=5).cell(self.field('@vessel_details_id.@imbarcazione_id.gt'),font_size='9pt', font_weight='bold')
        quinta_col.row(height=5).cell(self.field('@vessel_details_id.beam'),font_size='9pt', font_weight='bold')
        quinta_col.row(height=5).cell(self.field('draft_fw_arr'),font_size='9pt', font_weight='bold')
        quinta_col.row(height=5).cell(self.field('@vessel_details_id.n_eliche_poppa'),font_size='9pt', font_weight='bold')

    def datiViaggio(self,row):
        prima_col = row.cell(width=20).layout(name='Viaggio', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=20)
        dativiaggio= "<div style='text-align: center;text-decoration:underline;padding: 10px 0;'>DATI VIAGGIO</div>" + '::HTML'
        prima_col.row(height=15).cell(dativiaggio, font_weight='bold', background='lightgrey')
        seconda_col = row.cell(width=40).layout(name='descr2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',width=40,content_class='cellheader')
        seconda_col.row(height=5).cell('PORTO DI PROVENIENZA ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('PREVISIONE DI ARRIVO ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('DESTINAZIONE ', font_weight='bold', background='lightgrey')

        terza_col = row.cell(width=70).layout(name='descr3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,
                                    lbl_height=3, style='line-height:5mm;',width=70,content_class='celldata')
        terza_col.row(height=5).cell(self.field('lastport'),font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('eta'),font_size='9pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('nextport'),font_size='9pt', font_weight='bold')

        quarta_col = row.cell(width=30).layout(name='descr4', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=30,content_class='cellheader')
        quarta_col.row(height=5).cell('DATA E ORA ', font_weight='bold', background='lightgrey')
        quarta_col.row().cell('PREVISIONE DI PARTENZA ', font_weight='bold', background='lightgrey')


        quinta_col = row.cell().layout(name='descr5', um='mm', border_color='black', lbl_class='',hasBorderTop=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='celldata')
        quinta_col.row(height=5).cell(self.field('departure_lp'),font_size='9pt', font_weight='bold')
        quinta_col.row().cell(self.field('ets'),font_size='9pt', font_weight='bold')

 
    def datiOperazioni(self,row):
        #qui prendiamo tutti i dati relativi al carico che poi saranno estartti con il ciclo for
        carico = self.record['@cargo_lu_arr']
        #qui verifichiamo il numero di record relaìtivi al carico per il calcolo altezze celle e padding delle descrizioni OPERAZIONI COMMERCIALI e CARICO
        h_car=len(carico)*5
        p_car=str(len(carico)*(len(carico)*1.2))
        p_oc=str(250+(len(carico)*(len(carico)*3)))
        prima_col = row.cell(width=10).layout(name='Operazioni', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
                                    row_border=False,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=10)
        datioper= "<div style='text-align: center;text-decoration:underline;padding: "+p_oc+"% 0;transform: rotate(-90deg);'>OPERAZIONI COMMERCIALI</div>" + '::HTML'
        prima_col.row().cell(datioper, font_weight='bold', background='lightgrey')
        seconda_col = row.cell().layout(name='descr2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=False,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        cel_cargoonboard=seconda_col.row(height=5).cell('CARICO A BORDO (**)', font_weight='bold', background='lightgrey',width=35)
        daticar= "<div style='text-align: center;padding:"+p_car+ "% 0;'>CARICO (**)</div>" + '::HTML'
        cel_cargo=seconda_col.row(height=h_car).cell(daticar, font_weight='bold', background='lightgrey',width=30)
        col3=cel_cargoonboard.row.cell().layout(name='col3', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        extra_cargo_onboard = ''
        if self.field('extra_cargo_onboard') is not None and self.field('extra_cargo_onboard') != '':
            extra_cargo_onboard = ' - ' + self.field('extra_cargo_onboard')                                    
        col3.row().cell("{cargoonboard}::HTML".format(cargoonboard=self.field('cargo_onboard') + extra_cargo_onboard),  font_weight='bold',font_size='8pt')
        col4=cel_cargo.row.cell().layout(name='col4', um='mm', border_color='black', lbl_class='',row_border=False,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader') 
        
        #con il ciclo for andiamo a prelevare i dati del carico e inseriamo le singole righe
        for c in carico.values():
            r = col4.row(height=5)
            if c['extra_description_cp'] is not None:
                extra_descr_car = " - " + c['extra_description_cp']
            else:
                extra_descr_car = '' 
            if c['operation'] == 'U':
                oper = 'DA SCARICARE: '
            elif c['operation'] == 'L':
                oper = 'DA CARICARE: '  
            else:
                oper=''
            if c['@measure_id.description'] is not None:
                cargo_ms = c['@measure_id.description']
            else:
                cargo_ms = ''
            if c['quantity'] is not None:
                quantity=c['quantity']
            else:
                quantity='' 
            if c['description_it'] is not None and c['description_it'] != '':
                car_description = c['description_it']
            else:
                car_description = 'NIL'               
            car = "{op}{ms}{qt} {car} {descr_cp}".format(op=oper,ms=cargo_ms,qt=quantity,car=car_description, descr_cp=extra_descr_car)
            r.cell(car,font_weight='bold', font_size='8pt')
        if len(carico) == 0:
            r = col3.row(h_car)
            r.cell('NIL',font_weight='bold', font_size='8pt')
        cel_cargotransit=seconda_col.row(height=5).cell('CARICO IN TRANSITO (**)', font_weight='bold', background='lightgrey', width=40)
        col5=cel_cargotransit.row.cell().layout(name='col5', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader') 
        extra_cargo_transit = ''
        if self.field('extra_transit_cargo') is not None and self.field('extra_transit_cargo') !='':
            extra_cargo_transit = ' - ' + self.field('extra_transit_cargo')                            
        col5.row().cell("{cargotransit}::HTML".format(cargotransit=self.field('transit_cargo') + extra_cargo_transit),font_size='8pt', font_weight='bold')
        cel_ric_car=seconda_col.row(height=5).cell('RICEVITORE/CARICATORE', font_weight='bold', background='lightgrey',width=45)
        col6=cel_ric_car.row.cell().layout(name='col6', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col6.row(height=5).cell(self.field('ship_or_rec'),font_size='8pt', font_weight='bold')
        cel_nol=seconda_col.row(height=5).cell('NOLEGGIATORE', font_weight='bold', background='lightgrey',width=45)
        col7=cel_nol.row.cell().layout(name='col7', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col7.row(height=5).cell(self.field('chrtrs'),font_size='8pt', font_weight='bold')
        cel_moor=seconda_col.row(height=5).cell('ORMEGGIO RICHIESTO', font_weight='bold', background='lightgrey',width=45)
        col8=cel_moor.row.cell().layout(name='col8', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col8.row(height=5).cell(self.field('@dock_id.dock_name'),font_size='8pt', font_weight='bold')
        cel_lavori=seconda_col.row(height=5).cell('Per lavori o altri motivi', font_weight='bold', background='lightgrey',width=45)
        col9=cel_lavori.row.cell().layout(name='col9', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col9.row(height=5).cell(self.field('@extradatacp.lavori'),font_size='8pt', font_weight='bold')
        cel_notizie=seconda_col.row(height=5).cell('ALTRE NOTIZIE', font_weight='bold', background='lightgrey',width=45)
        col10=cel_notizie.row.cell().layout(name='col10', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col10.row(height=5).cell(self.field('@extradatacp.notizie'),font_size='8pt', font_weight='bold')
        cel_daywork=seconda_col.row(height=5).cell('GIORNI DI LAVORO', font_weight='bold', background='lightgrey',width=45)
        col11=cel_daywork.row.cell().layout(name='col11', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        cel_dw=col11.row(height=5).cell(self.field('@extradatacp.daywork'),font_size='8pt', font_weight='bold')
        col_ol=cel_dw.row.cell().layout(name='col_ol', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col_ol.row().cell('ORARIO DI LAVORO', background='lightgrey', font_weight='bold')
        col_tw=cel_dw.row.cell().layout(name='col_tw', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='celldata')
        col_tw.row().cell(self.field('@extradatacp.timework'),font_size='8pt', font_weight='bold')

    def datiOperazioni2(self,row):
        prima_col = row.cell(width=10).layout(name='Operazioni2', um='mm', border_color='black', lbl_class='',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=10)
        datioper= "<div style='text-align: center;padding: 0px 0;'></div>" + '::HTML'
        prima_col.row().cell(datioper, font_weight='bold', background='lightgrey')

        seconda_col = row.cell(width=45).layout(name='descr2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=False,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm; width=45',content_class='cellheader')
        seconda_col.row(height=5).cell('RICEVITORE/CARICATORE', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('NOLEGGIATORE', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('ORMEGGIO RICHIESTO', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('Per lavori o altri motivi', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('ALTRE NOTIZIE', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('GIORNI DI LAVORO', font_weight='bold', background='lightgrey')

        terza_col = row.cell().layout(name='descr3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=False,
                                    lbl_height=3, style='line-height:5mm;',content_class='celldata')
        terza_col.row(height=5).cell(self.field('ship_or_rec'),font_size='8pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('chrtrs'),font_size='8pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@dock_id.dock_name'),font_size='8pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@extradatacp.lavori'),font_size='8pt', font_weight='bold')
        terza_col.row(height=5).cell(self.field('@extradatacp.notizie'),font_size='8pt', font_weight='bold')
        cel_prova=terza_col.row(height=5).cell(self.field('@extradatacp.daywork'),font_size='8pt', font_weight='bold')
        col3=cel_prova.row.cell().layout(name='col3', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col3.row().cell('ORARIO DI LAVORO', background='lightgrey', font_weight='bold')
        col4=cel_prova.row.cell().layout(name='col4', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='celldata')
        col4.row().cell(self.field('@extradatacp.timework'),font_size='8pt', font_weight='bold')
        cel_prova=seconda_col.row(height=5).cell(self.field('@extradatacp.daywork'),font_size='8pt', font_weight='bold')


    def datiServizi(self,row):
        prima_col = row.cell(width=25).layout(name='Servizi', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=25)
        servizi= "<div style='text-align: center;text-decoration:underline;padding: 10px 0;'>DATI<br>SERVIZI</div>" + '::HTML'
        prima_col.row().cell(servizi, font_weight='bold', background='lightgrey')
        seconda_col = row.cell(width=35).layout(name='serv1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',width=35,content_class='cellheader', background='lightgrey')
        seconda_col.row(height=5).cell('PRATICO LOCALE ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('ORMEGGIATORI ', font_weight='bold', background='lightgrey')
        seconda_col.row(height=5).cell('RIMORCHIATORI ', font_weight='bold', background='lightgrey')

        terza_col = row.cell(width=5).layout(name='serv2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,
                                    lbl_height=3, style='line-height:5mm;',content_class='celldata')
                                
        if self.field('@extradatacp.pilot_arr') == 'Vero':
            pilot='X'
        else:    
            pilot=''
        if self.field('@extradatacp.moor_arr') == 'Vero':
            moor='X'
        else:    
            moor=''  
        if self.field('@extradatacp.tug_arr') == 'Vero':
            tug='X'
        else:    
            tug=''        
        terza_col.row(height=5).cell(pilot,font_size='8pt', font_weight='bold', style="text-align:center")
        terza_col.row(height=5).cell(moor,font_size='8pt', font_weight='bold', style="text-align:center")
        terza_col.row(height=5).cell(tug,font_size='8pt', font_weight='bold', style="text-align:center")

        quarta_col = row.cell(width=40).layout(name='serv3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',width=40,content_class='cellheader', background='lightgrey')
        quarta_col.row(height=5).cell('PRATICO LOCALE VHF', font_weight='bold', background='lightgrey')
        quarta_col.row(height=5).cell('NUMERO', font_weight='bold', background='lightgrey')
        quarta_col.row(height=5).cell('NUMERO', font_weight='bold', background='lightgrey')

        quinta_col = row.cell(width=5).layout(name='serv4', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,
                                    lbl_height=3, style='line-height:5mm;',content_class='celldata')
        if self.field('@extradatacp.pilot_arr_vhf') == 'Vero':
            pilotvhf='X'
        else:    
            pilotvhf=''
        quinta_col.row(height=5).cell(pilotvhf,font_size='8pt', font_weight='bold', style="text-align:center")
        quinta_col.row(height=5).cell(self.field('@extradatacp.n_moor_arr'),font_size='8pt', font_weight='bold', style="text-align:center")
        quinta_col.row(height=5).cell(self.field('@extradatacp.n_tug_arr'),font_size='8pt', font_weight='bold', style="text-align:center")
        sesta_col = row.cell(width=30).layout(name='serv5', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',width=30,content_class='cellheader', background='lightgrey')
        sesta_col.row(height=5).cell('ANTINCENDIO', font_weight='bold', background='lightgrey')
        settima_col = row.cell(width=5).layout(name='serv6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,
                                    lbl_height=3, style='line-height:5mm;',content_class='celldata')
        if self.field('@extradatacp.antifire_arr') == 'Vero':
            antincendio='X'
        else:    
            antincendio=''
        settima_col.row(height=5).cell(antincendio,font_size='8pt', font_weight='bold', style="text-align:center")
        ottava_col = row.cell(width=38).layout(name='serv7', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',width=38,content_class='cellheader', background='lightgrey')
        ottava_col.row(height=5).cell('ANTINQUINAMENTO', font_weight='bold', background='lightgrey')
        nona_col = row.cell(width=5).layout(name='serv8', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,
                                    lbl_height=3, style='line-height:5mm;',content_class='celldata')
        if self.field('@extradatacp.antipol_arr') == 'Vero':
            antinquinamento='X'
        else:    
            antinquinamento=''
        nona_col.row(height=5).cell(antinquinamento,font_size='8pt', font_weight='bold', style="text-align:center")
    
    
                              
    def datiExtra(self, row):
        extra = ("<div style='font-height: 8pt;'><u>Si dichiara che i servizi hanno assicurato la loro presenza nell'ora e nel numero sopra indicato</u></div>" )
        dati_layout = row.cell().layout(name='datiExtra', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:1,5mm;')
        extra1 = ("(*) Tipo della nave: M/n - Ro-Ro - Cisterna - M/gas. - P/ne - R/re - S/V - ecc." )
        extra2 =  "<br>(**) - Se trattasi di merci pericolose precisare la classe IMO"
        extra3 = "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- se trattasi di merci secche pericolose indicare per esteso l'esatta denominazione tecnica e la classe di pericolosità"
        extra4 = "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- se trattasi di altre merci secche, precisare se alla rinfusa e l'appendice di appartenenza (A-B-C) qualora soggette al D.M. 22.07.1991 + IMSBC CODE"
        extra5 = "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- se trattasi di merce rientrante nelle categorie inquinanti di cui alla Legge 979/1982 specificare tutti I dati relativi al proprietario"

        dati_layout.row(height=25).cell(extra + extra1 + extra2 + extra3 + extra4 + extra5 +'::HTML',font_size='6pt')

    def datiFirma(self, row):
        annotazioni=row.cell().layout(name='annotazioni', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        ann_cp = "ANNOTAZIONI DELL'AUTORITÀ MARITTIMA<br>"
        ann_cp1 = "Presentata alle ore________ del___________<br>"
        ann_cp2 = "Ormeggio assegnato ____________________<br>"
        ann_cp3 = "Ora assegnata di entrata_________________"

        annotazioni.row().cell(ann_cp + ann_cp1 + ann_cp2 + ann_cp3 + '::HTML', font_weight='bold')
        firma = row.cell().layout(name='firma', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        
        firma.row().cell('FIRMA', font_size='14pt',content_class='aligned_center')
        timbro=self.record['@agency_id.agency_stamp']
        #timbro=self.page.externalUrl(stamp) #se l'immagine è salvata dentro la cartella site
        firma.row(height=15).cell("""<img src="%s" width="auto" height="30mm">::HTML""" %timbro,width=0,content_class='aligned_center')
        
    
        #print(x)
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
        
        return 'Domanda_Accosto.{ext}'.format(ext=ext)

        #return 'Scheda cliente_{cliente}.{ext}'.format(cliente=self.record['reference_num'], ext=ext)
