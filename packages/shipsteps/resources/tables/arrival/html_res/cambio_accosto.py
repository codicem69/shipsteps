#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-
#
#  Stampa Comunicazione di Partenza CP


from turtle import width
from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime
from datetime import datetime, tzinfo
from dateutil import tz
import pytz

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
                            um='mm',top=5,left=4,right=4, bottom=3,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='9pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='black')
        

       # layout.row(height=10).cell("<div style='font-size:20pt;padding:5px'><strong>Dati Anagrafici</strong></div>::HTML")
        dati_agenzia = layout.row(height=25, lbl_height=2, lbl_class='smallCaption')
        #layout.row(height=10).cell()
        dati_cp = layout.row(height=20, lbl_height=4, lbl_class='smallCaption')
        layout.row(height=7).cell("<div style='font-size:14pt;padding:5px;text-align: center'><strong>COMUNICAZIONE DI CAMBIO ACCOSTO</strong></div>::HTML")
        dati_mandato = layout.row(height=30, lbl_height=4, lbl_class='smallCaption')
        dati_nave = layout.row(height=40, lbl_height=4, lbl_class='smallCaption')
        dati_viaggio = layout.row(height=20, lbl_height=4, lbl_class='smallCaption')
        dati_operazioni = layout.row(height=25,lbl_height=4, lbl_class='smallCaption')
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
    
    def datiMandato(self, row):
        mandato = ("Il/la sottoscritto/a agente raccomandatario marittimo "+self.field('@agency_id.agent_name')+" nato/a a " + self.field('@agency_id.birthplace') + " domiciliato/a presso l'agenzia Marittima " + self.field('@agency_id.agency_name') + " tel. " + self.field('@agency_id.tel') + " cell. " + self.field('@agency_id.mobile_agent') + "<br>" + "<div style='text-align: center;'> premesso<br></div>" +
                   "di aver ricevuto mandato, ai sensi dell'art.3 Legge 04/04/1977 n.135 da: " + self.field('mandatory') +"<br>Armatore: "+self.field('@vessel_details_id.@owner_id.own_fullname')+
                    '<br>preannuncia la partenza della sottonotata nave:'+ '::HTML' )
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
        terza_col.row(height=5).cell(self.parameter('draft_poppa'),font_size='9pt', font_weight='bold')
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
        quinta_col.row(height=5).cell(self.parameter('draft_prua'),font_size='9pt', font_weight='bold')
        quinta_col.row(height=5).cell(self.field('@vessel_details_id.n_eliche_poppa'),font_size='9pt', font_weight='bold')

    def datiViaggio(self,row):
        prima_col = row.cell(width=20).layout(name='Viaggio', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=20)
        dativiaggio= "<div style='text-align: center;text-decoration:underline;padding: 10px 0;'>DATI VIAGGIO</div>" + '::HTML'
        prima_col.row(height=20).cell(dativiaggio, font_weight='bold', background='lightgrey')
        seconda_col = row.cell().layout(name='descr2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                   lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        cel_dest=seconda_col.row(height=5).cell('PROVENIENTE DALLA BANCHINA', font_weight='bold', background='lightgrey',width=55)
        col3=cel_dest.row.cell().layout(name='col3', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        cel_np=col3.row().cell(self.parameter('dock_name'),font_size='9pt', font_weight='bold')
        

        cel_part=seconda_col.row(height=5).cell('CAMBIO ACCOSTO DATA, ORA', font_weight='bold', background='lightgrey',width=55)
        col_etca=cel_part.row.cell().layout(name='col_etca', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
       
        dt_str = self.parameter('datetime_ca').strftime("%m/%d/%Y %H:%M:%S")
        dt_utc = datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S")
        
        dt_utc = dt_utc.replace(tzinfo=pytz.UTC)
        # Get local timezone
        local_zone = tz.tzlocal()
        # Convert timezone of datetime from UTC to local
        dt_local = dt_utc.astimezone(local_zone)
        local_time_str = dt_local.strftime("%d/%m/%Y, %H:%M")
        cel_etca=col_etca.row().cell(local_time_str,font_size='9pt', font_weight='bold')
        
        cel_orm_descr=seconda_col.row(height=5).cell('BANCHINA RICHIESTA', font_weight='bold', background='lightgrey',width=55)
        col_orm=cel_orm_descr.row.cell().layout(name='col_orm', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col_orm.row().cell(self.field('@dock_id.dock_name'),font_size='9pt', font_weight='bold')
        cel_orm_extra=seconda_col.row(height=5).cell('Ulteriori informazioni', font_weight='bold', background='lightgrey',width=55)
        col_orm_extra=cel_orm_extra.row.cell().layout(name='col_orm_extra', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col_orm_extra.row().cell(self.parameter('extra_info'),font_size='9pt', font_weight='bold')
      # seconda_col = row.cell(width=45).layout(name='descr2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
      #                             lbl_height=3, style='line-height:5mm;',width=45,content_class='cellheader')
      # seconda_col.row(height=5).cell('PORTO DI DESTINAZIONE ', font_weight='bold', background='lightgrey')
      # seconda_col.row(height=5).cell('PREVISIONE DI PARTENZA ', font_weight='bold', background='lightgrey')
      # seconda_col.row(height=5).cell('BANCHINA DI ORMEGGIO', font_weight='bold', background='lightgrey')

      # terza_col = row.cell(width=70).layout(name='descr3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,
      #                             lbl_height=3, style='line-height:5mm;',width=70,content_class='celldata')
      # terza_col.row(height=5).cell(self.field('nextport'),font_size='9pt', font_weight='bold')
      # terza_col.row(height=5).cell(self.field('eta'),font_size='9pt', font_weight='bold')
      # terza_col.row(height=5).cell(self.field('@dock_id.dock_name'),font_size='9pt', font_weight='bold')

      # quarta_col = row.cell(width=30).layout(name='descr4', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
      #                             vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=30,content_class='cellheader')
      # quarta_col.row(height=5).cell('ETA ', font_weight='bold', background='lightgrey')

      # quinta_col = row.cell().layout(name='descr5', um='mm', border_color='black', lbl_class='',hasBorderTop=True,
      #                             vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='celldata')
      # quinta_col.row(height=5).cell(self.field('eta_np'),font_size='9pt', font_weight='bold')
        

 
    def datiOperazioni(self,row):
        
        prima_col = row.cell(width=10).layout(name='Operazioni', um='mm', border_color='black', lbl_class='',hasBorderTop=True,hasBorderLeft=True,
                                    row_border=False,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',width=10)
        datioper= "<div style='text-align: center;text-decoration:underline;padding: 140% 0;-webkit-transform: rotate(-90deg);'>OPERAZIONI COMMERCIALI</div>" + '::HTML'
        prima_col.row().cell(datioper, font_weight='bold', background='lightgrey')
        seconda_col = row.cell().layout(name='descr2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        cel_cargoonboard=seconda_col.row(height=5).cell('CARICO A BORDO (**)', font_weight='bold', background='lightgrey',width=35)
        
        col3=cel_cargoonboard.row.cell().layout(name='col3', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        if self.parameter('carbordo_extra') is not None:
            carbordo_extra = ' - ' + str(self.parameter('carbordo_extra'))
        else:
            carbordo_extra = ''
        col3.row().cell("{cargoonboard}::HTML".format(cargoonboard=str(self.parameter('carbordo'))+carbordo_extra),  font_weight='bold',font_size='8pt')
        
        
        
        
        cel_ric_car=seconda_col.row(height=5).cell('RICEVITORE/CARICATORE', font_weight='bold', background='lightgrey',width=45)
        col6=cel_ric_car.row.cell().layout(name='col6', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col6.row(height=5).cell(self.field('ship_or_rec'),font_size='8pt', font_weight='bold')
        cel_nol=seconda_col.row(height=5).cell('NOLEGGIATORE', font_weight='bold', background='lightgrey',width=45)
        col7=cel_nol.row.cell().layout(name='col7', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col7.row(height=5).cell(self.field('chrtrs'),font_size='8pt', font_weight='bold')
        
        cel_lavori=seconda_col.row(height=5).cell('Per lavori o altri motivi', font_weight='bold', background='lightgrey',width=45)
        col9=cel_lavori.row.cell().layout(name='col9', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col9.row(height=5).cell(self.field('@extradatacp.lavori'),font_size='8pt', font_weight='bold')
        cel_notizie=seconda_col.row(height=5).cell('ALTRE NOTIZIE', font_weight='bold', background='lightgrey',width=45)
        col10=cel_notizie.row.cell().layout(name='col10', um='mm', border_color='black', lbl_class='',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col10.row(height=5).cell(self.field('@extradatacp.notizie'),font_size='8pt', font_weight='bold')

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
                    
        if self.parameter('pilota') == True:
            pilot='X'
        else:    
            pilot=''
        if self.parameter('moor') == True:
            moor='X'
        else:    
            moor=''  
        if self.parameter('tug') == True:
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
        if self.parameter('pilota_vhf') == True:
            pilotvhf='X'
        else:    
            pilotvhf=''
        quinta_col.row(height=5).cell(pilotvhf,font_size='8pt', font_weight='bold', style="text-align:center")
        quinta_col.row(height=5).cell(self.parameter('n_moor'),font_size='8pt', font_weight='bold', style="text-align:center")
        quinta_col.row(height=5).cell(self.parameter('n_tug'),font_size='8pt', font_weight='bold', style="text-align:center")
        sesta_col = row.cell(width=30).layout(name='serv5', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',width=30,content_class='cellheader', background='lightgrey')
        sesta_col.row(height=5).cell('ANTINCENDIO', font_weight='bold', background='lightgrey')
        settima_col = row.cell(width=5).layout(name='serv6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,
                                    lbl_height=3, style='line-height:5mm;',content_class='celldata')
        if self.parameter('antincendio') == True:
            antincendio='X'
        else:    
            antincendio=''
        settima_col.row(height=5).cell(antincendio,font_size='8pt', font_weight='bold', style="text-align:center")
        ottava_col = row.cell(width=42).layout(name='serv7', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    lbl_height=3, style='line-height:5mm;',width=42,content_class='cellheader', background='lightgrey')
        ottava_col.row(height=5).cell('ANTINQUINAMENTO', font_weight='bold', background='lightgrey')
        nona_col = row.cell(width=5).layout(name='serv8', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,
                                    lbl_height=3, style='line-height:5mm;',content_class='celldata')
        if self.parameter('antinquinamento') == True:
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
        ann_cp2 = "Ora assegnata di uscita_________________"

        annotazioni.row().cell(ann_cp + ann_cp1 + ann_cp2 + '::HTML', font_weight='bold')
        firma = row.cell().layout(name='firma', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;')
        
        firma.row().cell('FIRMA', font_size='14pt',content_class='aligned_center')
        stamp=self.record['@agency_id.agency_stamp']
        timbro=self.page.externalUrl(stamp)
        firma.row(height=15).cell("""<img src="%s" width="100" height="100">::HTML""" %timbro,width=0,content_class='aligned_center')
        
    
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
        return 'Cambio_Accosto.{ext}'.format(ext=ext)

        #return 'Scheda cliente_{cliente}.{ext}'.format(cliente=self.record['reference_num'], ext=ext)
