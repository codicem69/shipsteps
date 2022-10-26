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
                         $ship_or_rec,$caricoarrivo,$chrtrs"""
    #Con virtual_columns aggiungo a self.record anche le formulaColumn calcolate che altrimenti di default non verrebbero compilate 
    css_requires='general_decl'
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
        

        carico = self.record['@cargo_lu_arr']
        h_car=(len(carico)*5)+45

        layout.row(height=7).cell("<div style='font-size:14pt;padding:5px;text-align: center'><strong>IMO GENARAL DECLARATION</strong></div>::HTML")
        layout.row(height=7).cell("<div style='font-size:12pt;padding:5px;text-align: center'><strong>Arrivo/Arrival</strong></div>::HTML")
        dati_gd1 = layout.row(height=49.8,lbl_height=2, lbl_class='smallCaption')
        dati_gd2 = layout.row(height=h_car,lbl_height=2, lbl_class='smallCaption')
        dati_gd3 = layout.row(lbl_height=2, lbl_class='smallCaption')
        dati_firma = layout.row(lbl_height=4, lbl_class='smallCaption')
        
        self.datiGeneral1(dati_gd1)
        self.datiGeneral2(dati_gd2)
        self.datiGeneral3(dati_gd3)
        self.datiFirma(dati_firma)
        
    def datiGeneral1(self, row):
        
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col2 =  row.cell().layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:4mm;',content_class='cellheader')
        col1.row(height=10).cell(self.field('@vessel_details_id.@imbarcazione_id.nome'), font_weight='bold', lbl='1.1 Nome Nave - Name and type of ship')
       
        cel_port=col2.row(height=10).cell(self.field('@agency_id.@port.descrizione'), font_weight='bold',lbl='2.Porto di Arrivo - Port of arrival')
        col3=cel_port.row.cell().layout(name='col3', um='mm', border_color='black', lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col3.row(height=10).cell(self.field('@time_arr.moored'),font_size='9pt', font_weight='bold', lbl='3.Data e ora di Arrivo - Date time of arrival')
        
        cel_imo=col1.row(height=10).cell(self.field('@vessel_details_id.@imbarcazione_id.imo'), font_weight='bold', lbl='1.2 Imo no.', width=48)
        col_cs=cel_imo.row.cell().layout(name='col_cs', um='mm', border_color='black', lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col_cs.row(height=10).cell(self.field('@vessel_details_id.callsign'), font_weight='bold', lbl='1.3 Call Sign')
       
        cel_lp=col2.row(height=10).cell(self.field('lastport'), font_weight='bold',lbl='6.Porto di provenienza - Last port of call')
        col_lpdep=cel_lp.row.cell().layout(name='col_lpdep', um='mm', border_color='black', lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader_sp')
        col_lpdep.row().cell(self.field('departure_lp'),font_size='9pt', font_weight='bold', lbl="6.1 Data e ora di partenza luogo d'origine - Departure date and time of original place")
        
        cel_flag=col1.row(height=10).cell(self.field('@vessel_details_id.@imbarcazione_id.bandiera'), font_weight='bold', lbl='4.Bandiera - Flag State of ship', width=48)
        col_master=cel_flag.row.cell().layout(name='col_master', um='mm', border_color='black', lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col_master.row().cell(self.field('master_name'),font_size='9pt', font_weight='bold', lbl="5.Nome Comandante - Name of master")
        
        agenzia = (self.field('@agency_id.agency_name') + '<br>'+self.field('@agency_id.address') + '<br>Tel.: ' + self.field('@agency_id.tel') + '<br>Fax:' +
                    self.field('@agency_id.fax') + '<br>' + self.field('@agency_id.email') + '<br>' + self.field('@agency_id.web') + '::HTML')
        col2.row(height=29.8).cell(agenzia,font_size='9pt', font_weight='bold', lbl="8. Name and contact details of ship’s agent")
        registration = str(self.field('@vessel_details_id.@reg_place.descrizione')) + ' - ' + str(self.field('@vessel_details_id.@reg_place.@nazione_code.nome')) + ' / ' + str(self.field('@vessel_details_id.reg_num'))
        col1.row(height=10).cell(registration, font_weight='bold', 
                                        lbl="7.Certificato d'iscrizione (porto, data, numero) Certificate of registry (Port; date; number)")
        #cel_imo.row.cell(self.field('@vessel_details_id.@imbarcazione_id.bandiera'), font_weight='bold', lbl='4.Bandiera - Flag State of ship', width=45)
       #col_gt=cel_reg.row.cell().layout(name='col_gt', um='mm', border_color='black', lbl_class='smallCaption',
       #                            vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        cel_gt=col1.row(height=10).cell(self.field('@vessel_details_id.@imbarcazione_id.gt'), font_weight='bold',lbl='9.Stazza Lorda / GT')
        col_nt=cel_gt.row.cell().layout(name='col_gt', um='mm', border_color='black', lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col_nt.row(height=10).cell(self.field('@vessel_details_id.@imbarcazione_id.nt'), font_weight='bold',lbl='10.Stazza Netta / NT')

    def datiGeneral2(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:4mm;',content_class='cellheader')
        col1.row(height=10).cell(self.field('@dock_id.dock_name'), font_weight='bold', lbl="11.Posizione della Nave in Porto - Position of the ship in the port (berth or station)")
        col1.row(height=10).cell(str(self.field('lastport')) + ' / ' + str(self.field('@agency_id.@port.descrizione')), font_weight='bold', 
                                lbl="""12. Breve descrizione del viaggio (scali precedenti e successivi, precisare dove verrà sbarcato il carico restante) 
                                       Brief particulars of voyage (previous and subsequent ports of call; underline where remaining cargo will be discharged)"""
                                       ,content_class='cellheader_sp')
                                           
        col1.row(height=10).cell(self.field('@extradatacp.mot_appr'), font_weight='bold', lbl="12/a. Motivo Approdo")
        
        #dati carico
        cargoonboard='A BORDO: ' + str(self.field('cargo_onboard')+'<br>')
        cargotransit='IN TRANSITO: ' + str(self.field('transit_cargo')+'<br>')
        #qui prendiamo tutti i dati relativi al carico che poi saranno estartti con il ciclo for
        carico = self.record['@cargo_lu_arr']
        #qui verifichiamo il numero di record relaìtivi al carico per il calcolo altezze celle e padding delle descrizioni OPERAZIONI COMMERCIALI e CARICO
        h_car=(len(carico)*5)+15


        #con il ciclo for andiamo a prelevare i dati del carico e inseriamo le singole righe
        car,oper='',''
        for c in carico.values():
            if c['operation'] == 'U':
                oper += 'DA SCARICARE: '
                car += "{op}{ms}{qt} {car}<br>".format(op=oper,ms=c['@measure_id.description'],qt=str(c['quantity']),car=c['description_it'])
            elif c['operation'] == 'L':
                oper += 'DA CARICARE: '
                car += "{op}{ms}{qt} {car}<br>".format(op=oper,ms=c['@measure_id.description'],qt=str(c['quantity']),car=c['description_it'])
            else:
                car=''
        
        if len(carico) == 0:
            car ='NIL'

        descr_car= cargoonboard + car + cargotransit + '::HTML'
        col1.row(h_car).cell(descr_car, font_weight='bold', lbl="13. Breve descrizione del carico - Brief description of the cargo")

    def datiGeneral3(self, row):
        col1 = row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col2 =  row.cell().layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:4mm;',content_class='cellheader')
        cel_crew=col1.row(height=10).cell(self.field('n_crew'), font_weight='bold', lbl="14.Numero dei membri dell'equipaggio - Number of crew (incl. master)", 
                                    width=48,content_class='cellheader_sp')
        col_crew=cel_crew.row.cell().layout(name='col_crew', um='mm', border_color='black', lbl_class='smallCaption',row_border=False,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        cel_pax=col_crew.row(height=10).cell(self.field('n_passengers'), font_weight='bold', lbl='15.Numero Passeggeri Number of passengers',content_class='cellheader_sp')
       #col_remarks=cel_pax.row.cell().layout(name='col_remarks', um='mm', border_color='black', lbl_class='smallCaption',
       #                            vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col2.row(height=10).cell('ETD: '+ str(self.field('ets')), font_weight='bold', lbl='16. Remarks')
        cel_att=col1.row(height=5).cell('Attached documents (indicate number of copies)', lbl="",content_class='cellcenter')
       # col_att=cel_att.row.cell().layout(name='col_att', um='mm', border_color='black', lbl_class='smallCaption',
       #                            vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        
        cel_car=col1.row(height=15).cell(self.parameter('cargo_decl'), font_weight='bold', lbl='17.Dichiarazione di Carico-Cargo Declaration', width=48, content_class='cell_att_doc')
        col_car=cel_car.row.cell().layout(name='col_car', um='mm', border_color='black', lbl_class='smallCaption',
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;',content_class='cellheader')
        cel_prov=col_car.row(height=15).cell(self.parameter('store_list'), font_weight='bold', lbl='18.Dichiarazione delle provviste di bordo - Ship’s Stores Declaration', content_class='cell_att_doc')
       #col_own=cel_prov.row.cell().layout(name='col_own', um='mm', border_color='black', lbl_class='smallCaption',
       #                            vertical_align= 'middle',lbl_height=3, style='line-height:3mm;',content_class='cellheader')
        owner=str(self.field('@vessel_details_id.@owner_id.own_name')) + '<br>' + str(self.field('@vessel_details_id.@owner_id.address_own')) + '::HTML'
        col2.row(height=20).cell(owner, font_weight='bold', lbl='Armatore Owners')
        cel_crew=col1.row(height=15).cell(self.parameter('crew_list'), font_weight='bold', lbl='19.Ruolo equipaggio - Crew List', width=48, content_class='cell_att_doc')
        col_crew=cel_crew.row.cell().layout(name='col_crew', um='mm', border_color='black', lbl_class='smallCaption',row_border=False,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;',content_class='cellheader')
        col_crew.row(height=15).cell(self.parameter('pax_list'), font_weight='bold', lbl='20.Lista passeggeri - Passenger List', content_class='cell_att_doc')
        
        stamp=self.record['@agency_id.agency_stamp']
        timbro=self.page.externalUrl(stamp)
        data_att = str(self.parameter('data_att').strftime("%d/%m/%Y"))
        col2.row(height=30).cell(data_att+'<br>'+"""<img src="%s" width="100" height="100">::HTML""" %timbro, font_weight='bold',
                    lbl='21. Data e firma del comandante, agente o funzionario autorizzato Date and signature of master, agent or authorized official', content_class='cellheader_sp')
        
        stamp=self.record['@agency_id.agency_stamp']
        timbro=self.page.externalUrl(stamp)
        #col2.row(height=15).cell("""<img src="%s" width="100" height="100">::HTML""" %timbro,width=0,content_class='aligned_center')

        cel_eff=col1.row(height=15).cell(self.parameter('crew_effects'), font_weight='bold', lbl="22.Dichiarazione degli effetti personali dell'equipaggio (*)-Crew’s Effects Declaration*",
                                     width=48, content_class='cell_att_doc')
        col_eff=cel_eff.row.cell().layout(name='col_eff', um='mm', border_color='black', lbl_class='smallCaption',row_border=False,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:5mm;',content_class='cellheader')
        col_eff.row(height=15).cell(self.parameter('healt_decl'), font_weight='bold', lbl='Dichiarazione marittima    di sanità - Maritime Declaration of Health*', content_class='cell_att_doc')

    

    def datiFirma(self, row):
        annotazioni=row.cell().layout(name='annotazioni', um='mm', border_color='black', lbl_class='smallCaption',row_border=False,cell_border=False,
                                    lbl_height=3, style='line-height:5mm;')
        annotazioni.row().cell("Formulario FAL dell'IMO n.1")
       
        firma = row.cell().layout(name='firma', um='mm', border_color='black', lbl_class='smallCaption',row_border=False,cell_border=False,
                                    lbl_height=3, style='line-height:5mm;')
        
        firma.row(height=15).cell("(*) Solo all'arrivo<br>on arrival only::HTML", content_class='aligned_right')
        
    def outputDocName(self, ext=''):
        vessel = self.record['@vessel_details_id.@imbarcazione_id.nome']
        return 'Fal1_arr_{vessel}.{ext}'.format(vessel=vessel,ext=ext)

       
