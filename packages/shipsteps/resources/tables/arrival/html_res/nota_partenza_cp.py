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
                         $ship_or_rec,$caricoarrivo,$chrtrs,@vessel_details_id.@ship_docs.@issued.citta_nazione,$logo_cp"""
    #Con virtual_columns aggiungo a self.record anche le formulaColumn calcolate che altrimenti di default non verrebbero compilate 
    css_requires='nota_arr'
    def main(self):
        self.datiDeclaration()
        #Nel metodo main specifichiamo tutti i metodi da eseguire: in questo caso solo un metodo schedaCliente totalmente customizzato

    def datiDeclaration(self):
        self.paperpage = self.getNewPage()
        layout = self.paperpage.layout(
                            um='mm',top=5,left=6,right=6, bottom=3,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='9pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='black')

        vess_docs = self.record['@vessel_details_id.@ship_docs']
        carico = self.record['@cargo_lu_arr']
        #con il ciclo for andiamo a prelevare i dati del carico e inseriamo le singole righe
       
        car_l=''
        y=1
        for c in carico.values():
            if c['operation'] == 'L':
                y += 1
                car_l += "{ms}{qt} {car}<br>".format(ms=c['@measure_id.description'],qt=c['quantity'],car=c['description_it'])
        #print(x)
        if car_l:
            car = car_l
        else:
            car = 'NIL'
        if len(carico) == 0:
            car ='NIL'
        if y == 1:
            h_row = 3.5 + (y * 4.5)
        else:
            h_row = y * 3.6

        porto = self.field('@agency_id.@port.descrizione')
        #logo_cp=self.db.application.getPreference('logo_cp',pkg='shipsteps')
        #logocp=self.page.externalUrl(logo_cp)
        logocp = self.field('logo_cp')
        layout.row(height=15).cell("""<img src="%s" style="width: 84px; height: 71px;::HTML""" %logocp ,content_class="center")
        #layout.row(height=15).cell("""<img src="http://127.0.0.1:8082/_storage/site/image/LogoCP.jpg" style="width: 84px; height: 71px;::HTML""",content_class="center")
        layout.row(height=3).cell("<div style='font-size:8pt;padding:2px;text-align: center'><strong> </strong></div>::HTML")
        layout.row(height=3).cell("<div style='font-size:8pt;padding:2px;text-align: center'><strong><u>CAPITANERIA DI PORTO DI "+porto.upper()+"</u></strong></div>::HTML")
        layout.row(height=3).cell("<div style='font-size:8pt;padding:2px;text-align: center'><strong>DICHIARAZIONE INTEGRATIVA DI PARTENZA</strong></div>::HTML")
        layout.row(height=3).cell("<div style='font-size:6pt;padding:1px;text-align: center'><strong>Additional Declaration of Departure</strong></div>::HTML")
        layout.row(height=7).cell("<div style='font-size:8pt;padding:3px;text-align: center'>SPAZIO RISERVATO ALL’UFFICIO – PRATICA DI PARTENZA<br>Reserved to Office – Departure</div>::HTML").layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,hasBorderRight=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        dati_gd1 = layout.row(height=36,lbl_height=2, lbl_class='smallCaption')
        dati_gd2 = layout.row(height=6,lbl_height=2, lbl_class='smallCaption')
        dati_gd3 = layout.row(height=6,lbl_height=2, lbl_class='smallCaption')
        dati_gd4 = layout.row(height=6,lbl_height=2, lbl_class='smallCaption')
        dati_gd5 = layout.row(height=49+h_row,lbl_height=2, lbl_class='smallCaption')
        #dati_gd6 = layout.row(height=12,lbl_height=2, lbl_class='smallCaption')
        dati_gd7 = layout.row(height=30,lbl_height=2, lbl_class='smallCaption')
        dati_firma = layout.row(height=41,lbl_height=18, lbl_class='smallCaption')
        dati_autor = layout.row(height=10,lbl_height=2, lbl_class='smallCaption')



        self.datiGeneral1(dati_gd1)
        self.datiGeneral2(dati_gd2)
        self.datiGeneral3(dati_gd3)
        self.datiGeneral4(dati_gd4)
        self.datiGeneral5(dati_gd5, car, h_row)
        #self.datiGenaral6(dati_gd6, vess_docs)
        self.datiGenaral7(dati_gd7)
        self.datiFirma(dati_firma)
        self.datiAutorita(dati_autor)


    def datiGeneral1(self, row):
        
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;font-size:8pt;',content_class='celldata')
        col2 =  row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:4mm;font-size:8pt;',content_class='celldata')
        reg_arr = """Ricevuta il______________<br>Alle ore________________<br>N________registro PARTENZE<br>N________registro ARRIVI<br><br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;___________________________
        <br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;&ensp;(timbro e firma dell’ Autorità marittima) ::HTML"""

        col1.row(height=35).cell(reg_arr, lbl='')
        cel_port=col2.row(height=10).cell("(ART.179 CODICE DELLA NAVIGAZIONE)<br>(ART.179 CODE OF NAVIGATION)::HTML", lbl='')

        tributi = """<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;(Eventuale) Rivisto Partire <br><br><br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;___________________________
        <br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;&ensp;(timbro e firma dell’ Autorità marittima)""" + '::HTML'
        col2.row(height=25).cell(tributi, lbl="")


    def datiGeneral2(self, row):
        col1 = row.cell(width=80).layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=80,content_class='cellheader')
        col2 = row.cell(width=60).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=60,content_class='cellheader')
        col3 = row.cell().layout(name='col3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader')

        col1.row(height=6).cell(self.field('@vessel_details_id.@imbarcazione_id.nome'), font_weight='bold', lbl="NOME NAVE - Ship's Name",width=80)
        col2.row(height=6).cell(self.field('@vessel_details_id.callsign'), font_weight='bold', lbl="Nominativo Internaz. – Call Sign",width=60)
        col3.row(height=6).cell(self.field('@vessel_details_id.@imbarcazione_id.imo'), font_weight='bold', lbl="IMO Number")

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
        col4.row(height=6).cell(self.field('@vessel_details_id.type'), font_weight='bold', lbl="Tipo di nave – Type of ship")

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
        col1.row(height=10).cell(owner, font_weight='bold', lbl="Nome armatore - Nazionalità e indirizzo / Ship Owner  – Nationality and address")
        col1.row(height=7).cell(self.field('cargo_onboard_dep') + '::HTML', font_weight='bold', lbl="Carico a bordo - Tipo di carico – Merci pericolose / Cargo on board – Type of cargo – Dangerous goods")

        col1.row(h_row).cell(car + '::HTML', font_weight='bold', lbl="Carico imbarcato - Tipo di carico – Merci pericolose / Cargo loaded – Type of cargo – Dangerous goods")
        col1.row(height=7).cell(self.parameter('car_deck'), font_weight='bold', lbl="Carico imbarcato sopra coperta - Tipo di carico / Cargo loaded  on Deck – Type of cargo")
        cel_pass=col1.row(7).cell(self.field('@extradatacp.pax_dep'), font_weight='bold', lbl="Passeggieri a bordo – Passengers on board")
        col_pass=cel_pass.row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_p2')
        col_pass.row(height=7).cell(self.field('@extradatacp.pax_imb'), font_weight='bold', lbl='Passeggeri imbarcati – Passengers embarked')
        cel_arr=col1.row(height=7).cell(self.field('ets'), font_weight='bold', lbl="Prevista partenza – Expected departure")
        col_arr=cel_arr.row.cell(width=140).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=140,content_class='cellheader_p2')
        cel_prov=col_arr.row(height=7).cell(self.field('nextport'), font_weight='bold', lbl="Destinazione – Next port of call")
        col_prov=cel_prov.row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_p2')
        col_prov.row(height=7).cell(self.field('eta_np'), font_weight='bold', lbl="Arrivo (data/ora) – Arrival (date/time)")
        cel_berth=col1.row(height=7).cell(self.field('@dock_id.dock_name'), font_weight='bold', lbl="Posizione della nave in porto – Harbour Ship’s position")
        col_berth=cel_berth.row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_p2')
        col_berth.row(height=7).cell(self.parameter('hazmat'), font_weight='bold', lbl="- HAZMAT N° (se necessario – if necessary):")



    def datiGenaral7(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',content_class='cellheader_p2')
        col1.row(height=6).cell('Dichiarazione del Comandante – Captain’s declaration', font_weight='bold', lbl="")

        col1.row(height=20).cell("""DICHIARO di aver adempiuto ad ogni obbligo di sicurezza, di polizia, sanitario, fiscale, contrattuale e statistico.<br>
                                    I hereby DECLARE having fulfilled all safety, police, sanitary, fiscal, customs, contractual land statistic obligations<br>
                                    Dichiaro di essere a conoscenza degli avvisi ai naviganti vigenti per le zone di mare attraverso le quali la nave al mio commando si troverà a navigare.<br>
                                    I hereby DECLARE to be aware of all notice to mariners concerning waters where vessel under my command will navigate.<br>
                                    Dichiaro che la nave risponde ai prescritti criteri di stabilità e di assetto previsti dalla SOLAS’74 – Cap.II-I, parte B, Reg.8, para. 7.4.<br>
                                    I hereby DECLARE that stability and trimming of ship are in agreement with requirements of SOLAS’74, Chap.II-I, rule 8 para.7.4.::HTML""", lbl="")

    def datiFirma(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader')
        col1.row(height=6).cell(self.field('@agency_id.agency_name'), font_weight='bold', lbl="AGENZIA - AGENCY")
        col1.row(height=6).cell(self.field('master_name'), font_weight='bold', lbl="Nome e Cognome del Comandante – Name and surname fo the Master")
        cel_data=col1.row(height=25).cell(str(self.parameter('data_att').strftime("%d/%m/%Y")), font_weight='bold', lbl="Data/date")
        col_data=cel_data.row.cell(width=150).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',width=150,content_class='cellheader')
        stamp=self.parameter('vess_stamp')
        
        timbro=self.page.externalUrl(stamp)
        col_data.row(height=25).cell("""<img src="%s" width="auto" height="30mm">::HTML""" %timbro, font_weight='bold', lbl="Firma del Comandante, dell’agente o del funzionario autorizzato – Signature by master, authorized agent or officer")

    def datiAutorita(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:2mm;font-size:8pt;',content_class='cellheader_sp')
        col1.row(height=8).cell('SPAZIO RISERVATO ALLE ANNOTAZIONI DELL’AUTORITÀ MARITTIMA', lbl="")




    def outputDocName(self, ext=''):
        vessel = self.record['@vessel_details_id.@imbarcazione_id.nome']
        return 'Dich_integrativa_partenza_{vessel}.{ext}'.format(vessel=vessel,ext=ext)
        #return 'Dich_integrativa_partenza.{ext}'.format(ext=ext)
