#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-
#
#  Stampa general declaration


from turtle import width
from gnr.web.gnrbaseclasses import TableScriptToHtml
import datetime

class Main(TableScriptToHtml):
    maintable = 'shipsteps.arrival'
    virtual_columns = """$cp_int,@agency_id.fullstyle,$nextport,@vessel_details_id.@owner_id.own_fullname,$lastport,$nextport,@cargo_lu_arr.cargo_lu_en_ita,
                         $ship_or_rec,$caricoarrivo,$chrtrs,@vessel_details_id.@ship_docs.@issued.citta_nazione"""
    #Con virtual_columns aggiungo a self.record anche le formulaColumn calcolate che altrimenti di default non verrebbero compilate 
    css_requires='nota_arr'
    def main(self):
        self.datiDeclaration()
        #Nel metodo main specifichiamo tutti i metodi da eseguire: in questo caso solo un metodo schedaCliente totalmente customizzato

    def datiDeclaration(self):
        self.paperpage = self.getNewPage()
        layout = self.paperpage.layout(
                            um='mm',top=5,left=4,right=4, bottom=3,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='9pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='black')

        vess_docs = self.record['@vessel_details_id.@ship_docs']
        carico = self.record['@cargo_lu_arr']
        #con il ciclo for andiamo a prelevare i dati del carico e inseriamo le singole righe
        car=''
        y=1
        for c in carico.values():
            if c['operation'] == 'U':
                y += 1
                car += "{ms}{qt} {car}<br>".format(ms=c['@measure_id.description'],qt=c['quantity'],car=c['description_it'])
                #oper = 'DA SCARICARE: '
            if c['operation'] is None:
                oper=''
            if car == '':
                car='NIL'
        if len(carico) == 0:
            car ='NIL'
        if y == 1:
            h_row = 3.5 + (y * 4.5)
        else:
            h_row = y * 3.6

        porto = self.field('@agency_id.@port.descrizione')

        layout.row(height=15).cell("""<img src="http://127.0.0.1:8082/_storage/site/image/LogoCP.jpg" style="width: 84px; height: 71px;::HTML""",content_class="center")
        layout.row(height=3).cell("<div style='font-size:8pt;padding:2px;text-align: center'><strong> </strong></div>::HTML")
        layout.row(height=3).cell("<div style='font-size:8pt;padding:2px;text-align: center'><strong><u>CAPITANERIA DI PORTO DI "+porto.upper()+"</u></strong></div>::HTML")
        layout.row(height=3).cell("<div style='font-size:8pt;padding:2px;text-align: center'><strong>ALTRE INFORMAZIONI AD USO DELL’AUTORITÀ MARITTIMA</strong></div>::HTML")
        layout.row(height=3).cell("<div style='font-size:6pt;padding:1px;text-align: center'><strong>Other information for Maritime Authority</strong></div>::HTML")
        layout.row(height=7).cell("<div style='font-size:8pt;padding:1px;text-align: center'>SPAZIO RISERVATO ALL’UFFICIO – PRATICA DI ARRIVO<br>Reserved to Office – Arrival</div>::HTML").layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,hasBorderRight=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        dati_gd1 = layout.row(height=36,lbl_height=2, lbl_class='smallCaption')
        dati_gd2 = layout.row(height=6,lbl_height=2, lbl_class='smallCaption')
        dati_gd3 = layout.row(height=6,lbl_height=2, lbl_class='smallCaption')
        dati_gd4 = layout.row(height=6,lbl_height=2, lbl_class='smallCaption')
        dati_gd5 = layout.row(height=46+h_row,lbl_height=2, lbl_class='smallCaption')
        dati_gd6 = layout.row(height=12,lbl_height=2, lbl_class='smallCaption')
        dati_gd7 = layout.row(height=20,lbl_height=2, lbl_class='smallCaption')
        dati_firma = layout.row(height=41,lbl_height=18, lbl_class='smallCaption')
        dati_autor = layout.row(height=10,lbl_height=2, lbl_class='smallCaption')
        dati_vuoto = layout.row(height=80-h_row,lbl_height=2, lbl_class='smallCaption')
        layout.row(height=8).cell("<div style='font-size:8pt;padding:2px;text-align: center'>PAGINA RISERVATA AI CERTIFICATI E DOCUMENTI DI BORDO<br>Documents and certificates</div>::HTML")
        dati_cert = layout.row(height=190,lbl_height=2, lbl_class='smallCaption')
        dati_firma_cert = layout.row(height=40,lbl_height=18, lbl_class='smallCaption')
        layout.row(height=8).cell("<div style='font-size:8pt;padding:2px;text-align: center'>SPAZIO RISERVATO ALLE ANNOTAZIONI DELL’AUTORITÀ MARITTIMA</div>::HTML")

        self.datiGeneral1(dati_gd1)
        self.datiGeneral2(dati_gd2)
        self.datiGeneral3(dati_gd3)
        self.datiGeneral4(dati_gd4)
        self.datiGeneral5(dati_gd5, car, h_row)
        self.datiGenaral6(dati_gd6, vess_docs)
        self.datiGenaral7(dati_gd7)
        self.datiFirma(dati_firma)
        self.datiAutorita(dati_autor)
        self.datiCertificati(dati_cert, vess_docs)
        self.datiFirmaCertificati(dati_firma_cert)

    def datiGeneral1(self, row):
        
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;font-size:8pt;',content_class='celldata')
        col2 =  row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:4mm;font-size:8pt;',content_class='celldata')
        reg_arr = """Ricevuta il______________<br>Alle ore________________<br>N________registro ARRIVI<br><br><br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;___________________________
        <br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;&ensp;(timbro e firma dell’ Autorità marittima) ::HTML"""

        col1.row(height=35).cell(reg_arr, lbl='')
        cel_port=col2.row(height=5).cell("TRIBUTI SPECIALI PAGATI:", lbl='')

        tributi = """- Euro 5,17&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Attestazione N.__________<br>- Euro 31,00&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                    del___________________<br>- Euro 62,00<br>- Euro 124,00<br><br><br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;___________________________
        <br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;&ensp;(timbro e firma dell’ Autorità marittima)""" + '::HTML'
        col2.row(height=30).cell(tributi, lbl="")


    def datiGeneral2(self, row):
        col1 = row.cell(width=80).layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=80,content_class='cellheader')
        col2 = row.cell(width=60).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=60,content_class='cellheader')
        col3 = row.cell().layout(name='col3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader')

        col1.row(height=6).cell(self.field('@vessel_details_id.@imbarcazione_id.nome'), font_weight='bold', lbl="NOME NAVE - Ship's Name",width=80)
        col2.row(height=6).cell(self.field('@vessel_details_id.callsign'), font_weight='bold', lbl="Nominativo Internaz. – Call Sign",width=60)
        col3.row(height=6).cell(self.field('@vessel_details_id.@imbarcazione_id.imo'), font_weight='bold', lbl="IMO Number",width=52)

    def datiGeneral3(self, row):
        col1 = row.cell(width=60).layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=60,content_class='cellheader')
        col2 = row.cell(width=50).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=50,content_class='cellheader')
        col3 = row.cell(width=40).layout(name='col3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=40,content_class='cellheader')
        col4 = row.cell().layout(name='col4', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader')

        col1.row(height=6).cell(self.field('@vessel_details_id.@imbarcazione_id.bandiera'), font_weight='bold', lbl="Bandiera - Flag",width=60)
        col2.row(height=6).cell(self.field('@vessel_details_id.@reg_place.descrizione'),font_weight='bold', lbl="Porto Iscrizione – Port Registry",width=50)
        col3.row(height=6).cell(self.field('@vessel_details_id.reg_num'), font_weight='bold', lbl="Matricola n° - Official number",width=40)
        col4.row(height=6).cell(self.field('@vessel_details_id.type'), font_weight='bold', lbl="Tipo di nave – Type of ship",width=42)

    def datiGeneral4(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader')
        col2 = row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader')
        col1.row(height=6).cell(self.field('@vessel_details_id.@imbarcazione_id.gt'), font_weight='bold', lbl="Tonnellate stazza lorda – Gross Tonnage")
        col2.row(height=6).cell(self.field('@vessel_details_id.@imbarcazione_id.nt'), font_weight='bold', lbl="Tonnellate stazza netta – Net Tonnage")

    def datiGeneral5(self, row,car, h_row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',content_class='cellheader')
        owner=str(self.field('@vessel_details_id.@owner_id.own_name')) + ' - ' + str(self.field('@vessel_details_id.@owner_id.address_own')) + '::HTML'
        col1.row(height=7).cell(owner, font_weight='bold', lbl="Nome armatore - Nazionalità e indirizzo / Ship Owner  – Nationality and address")
        col1.row(height=7).cell(self.field('cargo_onboard'), font_weight='bold', lbl="Carico a bordo – Tipo di carico - Merci pericolose / Cargo on board – Type of cargo – Dangerous goods")

        col1.row(h_row).cell(car + '::HTML', font_weight='bold', lbl="Carico da sbarcare – Tipo di carico - Merci pericolose / Cargo to discharge – Type of cargo – Dangerous goods")
        col1.row(height=7).cell(self.parameter('car_deck'), font_weight='bold', lbl="Carico da sbarcare sopra Coperta – Tipo di carico / Cargo to discharge over the deck – Type of cargo")
        cel_pass=col1.row(7).cell(self.field('n_passengers'), font_weight='bold', lbl="Passeggieri a bordo – Passengers on board")
        col_pass=cel_pass.row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_p2')
        col_pass.row(height=7).cell(self.parameter('pax_sba'), font_weight='bold', lbl='Passeggieri da sbarcare – Passengers to landing')
        cel_arr=col1.row(height=7).cell(self.field('@time_arr.moored'), font_weight='bold', lbl="Arrivo (data/ora) – Arrival (date/time)")
        col_arr=cel_arr.row.cell(width=140).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=140,content_class='cellheader_p2')
        provenienza = str(self.field('lastport') + ' - ' + self.field('departure_lp'))
        cel_prov=col_arr.row(height=7).cell(provenienza, font_weight='bold', lbl="Provenienza (luogo/data) – Last port call (name/date)")
        col_prov=cel_prov.row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_p2')
        col_prov.row(height=7).cell(self.field('ets'), font_weight='bold', lbl="Prevista partenza expected departure")
        cel_berth=col1.row(height=7).cell(self.field('@dock_id.dock_name'), font_weight='bold', lbl="Posizione della nave in porto – Harbour Ship’s position")
        col_berth=cel_berth.row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_p2')
        col_berth.row(height=7).cell(self.parameter('hazmat'), font_weight='bold', lbl="- HAZMAT N° (se necessario – if necessary):")
        cel_ta=col1.row(height=4).cell('Tassa di ancoraggio – Anchorages duties', lbl="")
        col_ta=cel_ta.row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_p2')
        col_ta.row(height=4).cell('Sopratassa - Overduties', lbl="")

    def datiGenaral6(self, row, vess_docs):
        ta_issued,ta_date,ta_expire = '','',''
        sta_issued,sta_date,sta_expire = '','',''

        for c in vess_docs.values():
            if c['cert'] == '21_ta':
                ta_issued = c['@issued.citta_nazione']       
                if c['date_cert']:
                    ta_date = c['date_cert'].strftime("%d/%m/%Y")
                else:
                    ta_date = ''
                if c['expire']:
                    ta_expire = c['expire'].strftime("%d/%m/%Y")
                else:
                    ta_expire = ''
            if c['cert'] == '22_sta':
                sta_issued = c['@issued.citta_nazione']    
                if c['date_cert']:
                    sta_date = c['date_cert'].strftime("%d/%m/%Y")
                else:
                    sta_date = ''
                if c['expire']:
                    sta_expire = c['expire'].strftime("%d/%m/%Y")
                else:
                    sta_expire = ''


       # print(v)

        col1 = row.cell(width=44).layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=44,content_class='cellheader')
        col2 = row.cell(width=25).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=25,content_class='cellheader')
        col3 = row.cell(width=27).layout(name='col3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=27,content_class='cellheader')
        col4 = row.cell(width=44).layout(name='col4', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=44,content_class='cellheader')
        col5 = row.cell(width=25).layout(name='col5', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=25,content_class='cellheader')
        col6 = row.cell().layout(name='col6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader')
        col1.row(height=6).cell(ta_issued, font_weight='bold', lbl="Pagata a - paid at")
        col2.row(height=6).cell(ta_date, font_weight='bold', lbl="In data - on date")
        col3.row(height=6).cell(ta_expire, font_weight='bold', lbl="Scadenza - valid until")
        col4.row(height=6).cell(sta_issued, font_weight='bold', lbl="Pagata a - paid at")
        col5.row(height=6).cell(sta_date, font_weight='bold', lbl="In data - on date")
        col6.row(height=6).cell(sta_expire, font_weight='bold', lbl="Scadenza - valid until")
        col1.row(height=6).cell('', font_weight='bold', lbl="Totale € - Total €")
        col2.row(height=6).cell('', font_weight='bold', lbl="Bolletta - Number")
        col3.row(height=6).cell('', font_weight='bold', lbl="Tipo tassa - Type")
        col4.row(height=6).cell('', font_weight='bold', lbl="Totale € - Total €")
        col5.row(height=6).cell('', font_weight='bold', lbl="Bolletta - Number")
        col6.row(height=6).cell('', font_weight='bold', lbl="Tipo tassa - Type")

    def datiGenaral7(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2.5mm;font-size:8pt;',content_class='cellheader_p2')
        col1.row(height=6).cell('Specificare se 12 mesi o 30gg. Stato/Estero, se Approdo o Transhipment. Specify if duties is annual or 30 days State/International, if overduties is on touch or Transhipment', font_weight='bold', lbl="")
        col1.row(height=7).cell(self.parameter('evento_str'), font_weight='bold', lbl="Evento straordinario o avaria – Extraordinary event or damage (*):")
        col1.row(height=6).cell("""(*) Se presente allegare la denuncia di evento straordinario e/o estratto dal giornale nautico 2^ parte.
                                    If present remember to attached declaration about extraordinary event and/or copy of log book.""", lbl="")

    def datiFirma(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader')
        col1.row(height=6).cell(self.field('@agency_id.agency_name'), font_weight='bold', lbl="AGENZIA - AGENCY")
        col1.row(height=6).cell(self.field('@agency_id.agent_name'), font_weight='bold', lbl="""Nome e Cognome del Comandante, dell’agente o del funzionario autorizzato –
                                        Name and Surname of master, authorized agent or officer""")
        cel_data=col1.row(height=25).cell(str(self.parameter('data_att').strftime("%d/%m/%Y")), font_weight='bold', lbl="Data/date")
        col_data=cel_data.row.cell(width=150).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=150,content_class='cellheader')
        stamp=self.record['@agency_id.agency_stamp']
        timbro=self.page.externalUrl(stamp)
        col_data.row(height=25).cell("""<img src="%s" width="100" height="100">::HTML""" %timbro, font_weight='bold', lbl="Firma del Comandante, dell’agente o del funzionario autorizzato – Signature by master, authorized agent or officer")

    def datiAutorita(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_sp')
        col1.row(height=8).cell('SPAZIO RISERVATO ALLE ANNOTAZIONI DELL’AUTORITÀ MARITTIMA', lbl="")

    def datiCertificati(self, row, vess_docs):
        col1 = row.cell(width=50).layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=50,content_class='cellheader_p2')
        col2 = row.cell(width=35).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=35,content_class='cellheader_p2')
        col3 = row.cell(width=16).layout(name='col3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=16,content_class='cellheader_p2')
        col4 = row.cell(width=16).layout(name='col4', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=16,content_class='cellheader_p2')
        col5 = row.cell(width=35).layout(name='col5', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=35,content_class='cellheader_p2')
        col6 = row.cell(width=15).layout(name='col6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=15,content_class='cellheader_p2')
        col7 = row.cell(width=25).layout(name='col6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=25,content_class='cellheader_p2')

        col1.row(height=13).cell('Tipo di certificato<br>Type of Certificate::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col2.row(height=13).cell('Rilasciato a<br>Issued at::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col3.row(height=13).cell('il<br>on::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col4.row(height=13).cell('Valido fino<br>Valid until::HTML', lbl="",font_weight='bold', style='line-height:3mm;',content_class='cellheader_pt')
        col5.row(height=13).cell('Visita annuale a<br>annual survey at::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col6.row(height=13).cell('Data visita annuale annual surv. date', lbl="",font_weight='bold')
        col7.row(height=13).cell('Note<br>Notes::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')

        #facciamo la lettura della tabella lookup dei certificati per avere la descrizione dei certificati
        certificati = self.db.table('shipsteps.ship_cert').query(columns='$code,$certificate').fetchAsDict('code')
        for c in vess_docs.values():
            if c['cert']:
                certificato = certificati[c['cert']]['certificate']#nel ciclo for nella tabella shipsdoc sostituiamo il codice certificato con la desccrizione del certificato

                if c['cert'] == '15_class':
                    col1.row(height=8).cell('Per le sole Navi Italiane - Concerning Italian Ship only', lbl="", font_weight='bold')
                    col2.row(height=8).cell('', lbl="")
                    col3.row(height=8).cell('', lbl="")
                    col4.row(height=8).cell('', lbl="")
                    col5.row(height=8).cell('', lbl="")
                    col6.row(height=8).cell('', lbl="")
                    col7.row(height=8).cell('', lbl="")
                if c['cert'] == '21_ta':
                    break
                col1.row(height=8).cell(certificato, lbl="")
                col2.row(height=8).cell(c['@issued.citta_nazione'], lbl="")
                if c['date_cert']:
                    col3.row(height=8).cell(c['date_cert'].strftime("%d/%m/%Y"), lbl="",content_class='cellheader_p2t')
                else:
                    col3.row(height=8).cell('', lbl="")
                if c['expire']:
                    col4.row(height=8).cell(c['expire'].strftime("%d/%m/%Y"), lbl="")
                else:
                    col4.row(height=8).cell('', lbl="")
                col5.row(height=8).cell(c['@annual_place.citta_nazione'], lbl="")
                if c['annual_date']:
                    col6.row(height=8).cell(c['annual_date'].strftime("%d/%m/%Y"), lbl="")
                else:
                    col6.row(height=8).cell('', lbl="")
                col7.row(height=8).cell(c['note'], lbl="")


    def datiFirmaCertificati(self,row):
        col1 = row.cell(width=25).layout(name='col_1', um='mm', border_color='white', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=25,content_class='cellheader_p2')
        col2 = row.cell().layout(name='col_2', um='mm', border_color='white', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',content_class='cellheader_datacert')
        col3 = row.cell(width=80).layout(name='col_3', um='mm', border_color='white', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=80,content_class='cellheader_p2')
        col1.row(height=8).cell('Data / Date',lbl='')
        col2.row(height=8).cell(str(self.parameter('data_att').strftime("%d/%m/%Y")), font_weight='bold', lbl="")
        col3.row(height=8).cell('Il Comandante, agente o funzionario<br>Signature by master, authorized agent or officer::HTML',lbl='')

        stamp=self.record['@agency_id.agency_stamp']
        timbro=self.page.externalUrl(stamp)
        col3.row(height=15).cell("""<img src="%s" width="100" height="100">::HTML""" %timbro,lbl='')

    def outputDocName(self, ext=''):
        return 'Nota_arrivo.{ext}'.format(ext=ext)
