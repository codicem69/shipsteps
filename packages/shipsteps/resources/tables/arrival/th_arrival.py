#!/usr/bin/python3
# -*- coding: utf-8 -*-

from turtle import left
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
from gnr.core.gnrlang import GnrException
import os.path
from gnr.core.gnrbag import Bag
from docx import Document
import os
import subprocess #per apertura file tramite programma di sistema

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        arrival = r.columnset('colset_arrival', name='Arrival', color='white',background='DarkSlateBlue', font_weight='bold')
        arrival.fieldcell('agency_id', width='7em')
        arrival.fieldcell('reference_num', width='7em')
        arrival.fieldcell('visit_id',width='8em')
        arrival.fieldcell('nsis_prot',width='8em')
        arrival.fieldcell('voy_n', width='4em')
        arrival.fieldcell('date', width='5em')
        arrival.fieldcell('vessel_details_id', width='15em', font_weight='bold')
        expect = r.columnset('colset_expect', name='Expected Times', color='white',background='SeaGreen', font_weight='bold')
        expect.fieldcell('eta', width='5em', Short=True)
        expect.fieldcell('etb', width='5em')
        expect.fieldcell('et_start', width='5em')
        expect.fieldcell('etc', width='5em')
        expect.fieldcell('ets', width='5em')
        draft = r.columnset('colset_draft', name='Draft', color='white',background='SaddleBrown', font_weight='bold')
        draft.fieldcell('draft_aft_arr', width='3em')
        draft.fieldcell('draft_fw_arr', width='3em')
        draft.fieldcell('draft_aft_dep', width='3em')
        draft.fieldcell('draft_fw_dep', width='3em')
        extra = r.columnset('colset_extra', name='Signature / Mandatory / Invoicing', color='white',background='Tan', font_weight='bold')
        extra.fieldcell('firma_div',width='5em')
        extra.fieldcell('mandatory', width='16em')
        extra.fieldcell('invoice_det_id', width='30em')
        berth = r.columnset('colset_berth', name='Berth', color='white',background='Gray', font_weight='bold')
        berth.fieldcell('dock_id', width='5em')
        berth.fieldcell('info_moor', width='6em')
        member = r.columnset('colset_member', name='People on board', color='white',background='DarkCyan', font_weight='bold')
        member.fieldcell('master_name', width='6em')
        member.fieldcell('n_crew', width='3em')
        member.fieldcell('n_passengers', width='3em', name='Pax no.')
        lastport = r.columnset('colset_lastport', name='Last Port', color='white',background='SlateGray', font_weight='bold')
        lastport.fieldcell('last_port', width='7em')
        lastport.fieldcell('departure_lp', width='5em')
        nextport = r.columnset('colset_nextport', name='Next Port', color='white',background='Maroon', font_weight='bold')
        nextport.fieldcell('next_port', width='7em')
        nextport.fieldcell('eta_np', width='5em')
        gpg = r.columnset('colset_gpg', name='GPG', color='Black',background='lightgray', font_weight='bold')
        gpg.fieldcell('@gpg_arr.n_gpg', name= 'GPG n.')
        gpg.fieldcell('@gpg_arr.date_start', name= 'GPG start', width='5em')
        gpg.fieldcell('@gpg_arr.date_end', name= 'GPG end', width='5em')
       #r.fieldcell('@cargo_lu_arr.description', name= 'cargo_descr', width='5em')
        #r.fieldcell('carico', name='Descrizione Carico',width='30em')
        #r.fieldcell('cargo', width='50em')
        #r.fieldcell('@cargo_lu_arr.cargo_on_board', width='50em')
        cargo = r.columnset('colset_cargo', name='Cargo', color='white',background='RosyBrown', font_weight='bold')
        cargo.fieldcell('cargo_dest')
        cargo.fieldcell('cargo_lu_en', width='30em')
        cargo.fieldcell('@cargo_lu_arr.tot_cargo', width='8em')
        cargo.fieldcell('ship_rec', width='30em')

    def th_order(self):
        return 'reference_num:d' 

    def th_query(self):
        return dict(column='reference_num', op='contains', val='', runOnStart=True)

    def th_options(self):
        return dict(view_preview_tpl='dati_nave')

class Form(BaseComponent):
    
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
    
        form.store.handler('load',virtual_columns='$workport')
        #pane = form.record
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        tc = form.center.tabContainer()
        #bc1 = form.center.borderContainer()
        #tc = bc1.tabContainer(margin='2px', region='center', height='auto', splitter=True)

        bc = tc.borderContainer(title='!![en]Arrival')
        bc_extracp = tc.borderContainer(title='!![en]Extra dati CP')
        bc_att = tc.borderContainer(title='!![en]Attachments')
        tc_task = tc.tabContainer(title='!![en]Task List',region='center',selectedPage='^.pippo')
        bc_tasklist = tc_task.borderContainer(title='!![en]Task List', region='center')
       # tc_task = tc_task.tabContainer(title='!![en]Shore Pass')
        #tc_shorepass = tc_task.tabContainer(title='!![en]Shore Pass', region='center')
        #tc_prova = tc_task.tabContainer(title='!![en]prova')
        tc_undertask = bc_tasklist.tabContainer(margin='2px', region='center', height='auto')
        tc_sof = tc.borderContainer(title='!![en]SOF')
        tc_app = tc.tabContainer(title='!![en]Applications')
        tc_bl = tc.borderContainer(title='!![en]Loading Cargoes')
        tc_usma = tc.borderContainer(title='!![en]Sanimare certificates')
        #tc_parapon = bc_task3.tabContainer(title='pippo')
        self.extraDatiCP(bc_extracp.borderContainer(region='center', splitter=True, background = 'seashell'))
        #self.usmaCert(bc_usma.borderContainer(title='!![en]Renew certificates Sanimare',region='center', splitter=True, background = 'seashell'))
        tc_bl.contentPane(title='!![en]Loading Cargoes',height='100%',pageName='sanimare_cert').remote(self.cargodocsCertLazyMode)
        tc_usma.contentPane(title='!![en]Renew certificates Sanimare',height='100%',pageName='sanimare_cert').remote(self.usmaCertLazyMode)

        self.allegatiArrivo(bc_att.contentPane(title='!![en]Attachments', height='100%'))
       # tc2 = bc2.tabContainer(margin='2px', region='center', height='auto', splitter=True)
       # bc_top = bc.borderContainer(region='center',height='300px', splitter=True)
       # pane_center=bc_top.contentPane(region='center',datapath='.record', width='1200px', splitter=True)
        #pane_center=bc_top.contentPane(region='center',datapath='.record', width='1100px', splitter=True)
       # pane_right=bc_top.contentPane(region='right',datapath='.@gpg_arr', width='320px', splitter=True)
        self.datiArrivo(bc.borderContainer(region='top',height='300px', splitter=True, background = 'seashell'))
       
        self.taskList(bc_tasklist.borderContainer(region='top',height='50%', background = 'seashell', splitter=True))
        #self.shorepass(tc_task.contentPane(title='!![en]Shore pass'))
        #self.services(tc_task.contentPane(title='!![en]Vessel Services',pageName='services'))
        
        tc_task.contentPane(title='!![en]Shore pass',pageName='shore_pass').remote(self.shorePassLazyMode)
        tc_task.contentPane(title='!![en]Vessel Services',pageName='services').remote(self.servicesLazyMode)
        
        #self.sof(tc_sof.contentPane(title='!![en]Sof',height='100%'))
        tc_sof.contentPane(title='!![en]Sof',height='100%').remote(self.sofLazyMode)
        
        #self.allegatiArrivo(tc_task.contentPane(title='Attachments', region='center', height='100%', splitter=True))
        
        self.garbage(tc_undertask.contentPane(title='!![en]Garbage'))
        #self.rinfusa(tc_app.contentPane(title='!![en]Bulk Application'))
        tc_app.contentPane(title='!![en]Bulk Application',pageName='bulk_application').remote(self.rinfusaLazyMode)
        #self.bunker(tc_app.contentPane(title='!![en]Bunker Application'))
        tc_app.contentPane(title='!![en]Bunker Application',pageName='bunker_application').remote(self.bunkerLazyMode)
        
        #self.datiArrivo(pane_center)
        #self.datiArrivo(pane_center)
        #self.gpg(bc.borderContainer(region='center',datapath='.@gpg_arr',height='300px', splitter=True, background = 'lavenderblush'))

        tc = bc.tabContainer(margin='2px', region='center', height='auto', splitter=True)
        tc_car = tc.tabContainer(title='!![en]Cargo',margin='2px', region='center', height='auto', splitter=True)
        #tc_sof = tc.tabContainer(title='!![en]SOF',margin='2px', region='center', height='450px', splitter=True)
        #tc_r = bc_top.tabContainer(margin='2px', region='right', width='25%')#, width='25%', splitter=True)
        #self.gpg(tc_r.contentPane(title='!![en]GPG'))
        tc_under_car = tc_car.tabContainer(title='!![en]Cargo onboard')
        #self.datiCaricoBordo(tc_car.contentPane(title='!![en]Cargo onboard',datapath='.record'))
        self.carbordoArr(tc_under_car.contentPane(title='!![en]Cargo onboard on arrival',datapath='.record'))
        self.carbordoDep(tc_under_car.contentPane(title='!![en]Cargo onboard on departure',datapath='.record'))

        self.datiCarico(tc_car.contentPane(title='!![en]Cargo loading / unloading'))
        self.datiCaricoTransit(tc_car.contentPane(title='!![en]Transit cargo',datapath='.record'))
        
      # tc.contentPane(title='!![en]Shippers / Receivers', pageName='shippers_receivers').remote(self.car_ricLazyMode)
      # tc.contentPane(title='!![en]Charterers', pageName='charterers').remote(self.charterersLazyMode)

       # self.sof(tc.contentPane(title='!![en]Sof'))
        self.arrival_details(tc.borderContainer(title='!![en]Arrival/Departure details', region='top', background = 'seashell'))
       # self.emailArrival(tc.contentPane(title='!![en]Email Arrival'))
        tc.contentPane(title='!![en]Email Arrival',pageName='email_arrival').remote(self.emailArrivalLazyMode)
        #self.taskList(tc.borderContainer(title='!![en]Task list', region='top', background = 'lavenderblush'))

        #self.sof_cargo(tc_sof.contentPane(title='!![en]Sof_Cargo', datapath='.@sof_arr'))
    def carbordoArr(self,bc):
        center = bc.roundedGroup(title='!![en]Cargo on board on arrival', region='center', height = '100%').div(margin='10px',margin_left='2px')
        fb = center.formbuilder(cols=3, border_spacing='4px')
        fb.field('cargo_onboard', tag='simpleTextArea',height='50px', colspan=3)
        fb.div("""EXTRA CARGO ON BOARD DESCRIPTION:<br>
                  - Se trattasi di merci pericolose precisare la classe IMO<br>
                  - se trattasi di merci secche pericolose indicare per esteso l'esatta denominazione tecnica e la classe di pericolosità<br>
                  - se trattasi di altre merci secche, precisare se alla rinfusa e l'appendice di appartenenza (A-B-C) qualora soggette al D.M. 22.07.1991 + IMSBC CODE<br>
                  - se trattasi di merce rientrante nelle categorie inquinanti di cui alla Legge 979/1982 specificare tutti I dati relativi al proprietario""", colspan=3)
        fb.field('extra_cargo_onboard', tag='simpleTextArea',height='25px',colspan=3)
    def carbordoDep(self,bc):
        center = bc.roundedGroup(title='!![en]Cargo on board on departure', region='center', height = '100%').div(margin='10px',margin_left='2px')
        fb = center.formbuilder(cols=3, border_spacing='4px')
        fb.field('cargo_onboard_dep', tag='simpleTextArea',height='50px', colspan=3)
        fb.div("""EXTRA CARGO ON BOARD DESCRIPTION:<br>
                  - Se trattasi di merci pericolose precisare la classe IMO<br>
                  - se trattasi di merci secche pericolose indicare per esteso l'esatta denominazione tecnica e la classe di pericolosità<br>
                  - se trattasi di altre merci secche, precisare se alla rinfusa e l'appendice di appartenenza (A-B-C) qualora soggette al D.M. 22.07.1991 + IMSBC CODE<br>
                  - se trattasi di merce rientrante nelle categorie inquinanti di cui alla Legge 979/1982 specificare tutti I dati relativi al proprietario""", colspan=3)
        fb.field('extra_cargo_onboard_dep', tag='simpleTextArea',height='25px',colspan=3)
    
    def extraDatiCP(self, bc):
        rg_extra = bc.roundedGroup(title='!![en]Extra data CP on Arrival/Departure',table='shipsteps.extradaticp', region='center',datapath='.record.@extradatacp',width='auto', height = 'auto').div(margin='10px',margin_left='2px')
        div_arrival=rg_extra.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>ARRIVAL</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_arrival.formbuilder(cols=5, border_spacing='4px',fld_width='10em')
        fb.radioButtonText(value='^.motivo_viaggio', values='op_com:Operazioni_Commerciali,altro:Altro', lbl='Motivo Viaggio: ',validate_notnull=True,width='20em',lbl_class='align_right')
        fb.radioButtonText(value='^.tipo_viaggio', values='linea:Di_Linea,occ:Occasionale', lbl='Tipo Viaggio: ',validate_notnull=True, width='20em')
        fb.field('mot_appr', width='20em', colspan=2)
        fb.br()
        fb.field('lavori', width='40em', colspan=2)
        fb.br()
        fb.field('notizie', width='40em', colspan=2)
        fb.br()
        fb.field('pilot_arr')
        fb.field('pilot_arr_vhf')
        fb.field('antifire_arr')
        fb.field('antipol_arr')
        fb.br()
        fb.field('moor_arr')
        fb.field('n_moor_arr')
        fb.field('tug_arr')
        fb.field('n_tug_arr')
        fb.br()
        fb.field('daywork', placeholder='eg. 3 giorni')
        fb.field('timework')
        fb.br()
        fb.field('naz_cte')
        fb.field('n_ita')
        fb.field('n_com')
        fb.field('n_excom')
        fb.br()
        fb.field('carmcycle_arr')
        fb.field('commveic_arr')

        div_departure=rg_extra.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>DEPARTURE</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_departure.formbuilder(cols=5, border_spacing='4px',fld_width='10em')
        fb.field('pilot_dep')
        fb.field('pilot_dep_vhf')
        fb.field('antifire_dep')
        fb.field('antipol_dep')
        fb.br()
        fb.field('moor_dep')
        fb.field('n_moor_dep')
        fb.field('tug_dep')
        fb.field('n_tug_dep')
        fb.br()
        fb.field('pax_dep')
        fb.field('pax_trans')
        fb.field('pax_sba')
        fb.field('pax_imb')
        fb.br()
        fb.field('carmcycle_dep')
        fb.field('carmcycle_trans')
        fb.field('carmcycle_sba')
        fb.field('carmcycle_imb')
        fb.br()
        fb.field('commveic_dep')
        fb.field('commveic_trans')
        fb.field('commveic_sba')
        fb.field('commveic_imb')
        fb.br()
        fb.field('car_imb',colspan=2, tag='textArea', width='36em')
        fb.field('car_sba',colspan=2, tag='textArea', width='36em')

    @public_method
    def servicesLazyMode(self,pane):
        pane.inlineTableHandler(relation='@vess_services',viewResource='ViewFromVesselServices',
                                view_store__onBuilt=True)

    def services(self,pane):
        #pass
        #pane.inlineTableHandler(relation='@garbage_arr',viewResource='ViewFromGarbage')
        pane.inlineTableHandler(relation='@vess_services',viewResource='ViewFromVesselServices')

    def datiArrivo(self,bc):
        center = bc.roundedGroup(title='!![en]Vessel arrival', region='center',datapath='.record',width='210px', height = '100%').div(margin='10px',margin_left='2px')
        center1 = bc.roundedGroup(title='!![en]Arrival details',region='center',datapath='.record',width='960px', height = '100%', margin_left='210px').div(margin='10px',margin_left='2px')
        center2 = bc.roundedGroup(title='!![en]Special security guards',table='shipsteps.gpg',region='center',datapath='.record.@gpg_arr',width='240px', height = '150px', margin_left='1170px').div(margin='10px',margin_left='2px')
        center3 = bc.roundedGroup(title='!![en]EXTRA',region='center',datapath='.record',width='240px',margin_left='1170px', margin_top='150px').div(margin='10px',margin_left='2px')
        #center3 = bc.roundedGroup(title='!![en]Times',table='shipsteps.arrival_time',region='center',datapath='.record.@time_arr',width='245px', height = '350px', margin_left='1385px').div(margin='10px',margin_left='2px')

        fb = center.formbuilder(cols=1, border_spacing='4px',lblpos='T')
        fb.field('agency_id', readOnly=True )
        fb.field('reference_num', readOnly=True)
        fb.field('date')
        fb.field('vessel_details_id',validate_notnull=True )
        fb.field('pfda_id' , hasDownArrow=True,  auxColumns='$data,@imbarcazione_id.nome',order_by='$data DESC')
        fb.field('visit_id')

        fb = center1.formbuilder(cols=5, border_spacing='4px',lblpos='T',fldalign='left')
        fb.field('eta' , width='10em')
        fb.field('etb' , width='10em')
        fb.field('et_start' , width='10em')
        fb.field('etc' , width='10em')
        fb.field('ets', width='10em' )
        fb.field('draft_aft_arr', width='5em', placeholder='eg:4 or 4,5')
        fb.field('draft_fw_arr' , width='5em', placeholder='eg:4 or 4,5')
        fb.field('draft_aft_dep' , width='5em', placeholder='eg:4 or 4,5')
        fb.field('draft_fw_dep' , width='5em', placeholder='eg:4 or 4,5')
        fb.field('dock_id' )
        fb.field('info_moor',width='30em', colspan=2 ,placeholder='e.g. Inizio ormeggio il ... ore ....')
        fb.field('master_name' )
        fb.field('n_crew' , width='5em',validate_regex=" ^[0-9]*$",validate_regex_error='Insert only numbers')
        fb.field('n_passengers' , width='5em',validate_regex=" ^[0-9]*$",validate_regex_error='Insert only numbers')
        fb.br()
        fb.field('last_port',auxColumns='@nazione_code.nome,$unlocode', limit=20 )
        fb.field('departure_lp' , width='10em')
        fb.field('next_port',auxColumns='@nazione_code.nome,$unlocode', limit=20 )
        fb.field('eta_np' , width='10em')
        fb.field('voy_n', width='10')
        fb.field('mandatory', colspan=3 , width='47em')
        fb.field('cargo_dest', colspan=2, width='29em' )
        fb.br()
        fb.field('invoice_det_id',colspan=5 ,width='78em', hasDownArrow=True)

        fb = center2.formbuilder(cols=1, border_spacing='4px', fld_width='10em')
        #fb.field('arrival_id')
        fb.field('date_start')
        fb.field('date_end')
        fb.field('n_gpg')

        fb = center3.formbuilder(cols=1, border_spacing='4px', fld_width='18em',lblpos='T')
        fb.field('nsis_prot')
        fb.field('firma_div', tag='textArea')

       #fb = center3.formbuilder(cols=1, border_spacing='4px', fld_width='8em')
       ##fb.field('arrival_id')
       #fb.field('eosp')
       #fb.field('aor')
       #fb.field('anchored')
       #fb.field('anchor_up')
       #fb.field('pob')
       #fb.field('first_rope')
       #fb.field('moored')
       #fb.field('gangway')
       #fb.field('free_p')
       #fb.field('pobd')
       #fb.field('last_line')
       #fb.field('sailed')
       #fb.field('cosp', lbl='CoSP')

   #def datiCaricoBordo(self,frame):
   #    frame.simpleTextArea(title='!![en]Cargo on board',value='^.cargo_onboard',editor=True,validate_notnull=True)
    def datiCaricoBordo(self,bc):
        center = bc.roundedGroup(title='!![en]Cargo on board', region='center', height = '100%').div(margin='10px',margin_left='2px')
        fb = center.formbuilder(cols=3, border_spacing='4px')
        fb.field('cargo_onboard', tag='simpleTextArea',height='50px', colspan=3)
        fb.div("""EXTRA CARGO ON BOARD DESCRIPTION:<br>
                  - Se trattasi di merci pericolose precisare la classe IMO<br>
                  - se trattasi di merci secche pericolose indicare per esteso l'esatta denominazione tecnica e la classe di pericolosità<br>
                  - se trattasi di altre merci secche, precisare se alla rinfusa e l'appendice di appartenenza (A-B-C) qualora soggette al D.M. 22.07.1991 + IMSBC CODE<br>
                  - se trattasi di merce rientrante nelle categorie inquinanti di cui alla Legge 979/1982 specificare tutti I dati relativi al proprietario""", colspan=3)
        fb.field('extra_cargo_onboard', tag='simpleTextArea',height='25px',colspan=3)

    def datiCarico(self,pane):
        pane.inlineTableHandler(relation='@cargo_lu_arr',viewResource='ViewFromCargoLU')

    def datiCaricoTransit(self,bc):
        center = bc.roundedGroup(title='!![en]Transit cargo', region='center', height = '100%').div(margin='10px',margin_left='2px')
        fb = center.formbuilder(cols=3, border_spacing='4px')
        fb.field('transit_cargo', tag='simpleTextArea',height='50px', colspan=3)
        fb.div("""EXTRA TRANSIT CARGO DESCRIPTION:<br>
                  - Se trattasi di merci pericolose precisare la classe IMO<br>
                  - se trattasi di merci secche pericolose indicare per esteso l'esatta denominazione tecnica e la classe di pericolosità<br>
                  - se trattasi di altre merci secche, precisare se alla rinfusa e l'appendice di appartenenza (A-B-C) qualora soggette al D.M. 22.07.1991 + IMSBC CODE<br>
                  - se trattasi di merce rientrante nelle categorie inquinanti di cui alla Legge 979/1982 specificare tutti I dati relativi al proprietario""", colspan=3)
        fb.field('extra_transit_cargo', tag='simpleTextArea',height='25px',colspan=3)
   
    @public_method
    def car_ricLazyMode(self,pane):
         pane.stackTableHandler(table='shipsteps.ship_rec', formResource='Form',view_store_onStart=True,view_store__onBuilt=True)

    def car_ric(self,pane):
         pane.stackTableHandler(table='shipsteps.ship_rec', formResource='Form',view_store_onStart=True)

        
    @public_method
    def charterersLazyMode(self,pane):
        pane.inlineTableHandler(table='shipsteps.charterers',datapath='#FORM.charterers',parentForm=False,saveButton=True,semaphore=True,viewResource='ViewFromCharterers',view_store_onStart=True,view_store__onBuilt=True)
        
    def charterers(self,pane):
        pane.inlineTableHandler(table='shipsteps.charterers',viewResource='ViewFromCharterers',view_store_onStart=True)

    @public_method
    def sofLazyMode(self,pane):
        pane.stackTableHandler(relation='@sof_arr',view_store__onBuilt=True)

    def sof(self,pane):
        pane.stackTableHandler(relation='@sof_arr')#, formResource='FormSof')

    def arrival_details(self, bc):
        rg_times = bc.roundedGroup(title='!![en]Arrival/Departure times',table='shipsteps.arrival_time',region='left',datapath='.record.@time_arr',width='350px', height = 'auto').div(margin='10px',margin_left='2px')
        rg_details = bc.roundedGroup(title='!![en]Arrival details',table='shipsteps.arrival_det', region='center',datapath='.record.@arr_details',width='350px', height = '100%',margin_left='350px').div(margin='10px',margin_left='2px')
        rg_details_dep = bc.roundedGroup(title='!![en]Departure details',table='shipsteps.arrival_det', region='center',datapath='.record.@arr_details',width='350px', height = '100%',margin_left='350px').div(margin='10px',margin_left='2px')
        #rg_extra = bc.roundedGroup(title='!![en]Extra data CP on Arrival/Departure',table='shipsteps.extradaticp', region='center',datapath='.record.@extradatacp',width='auto', height = 'auto', margin_left='550px').div(margin='10px',margin_left='2px')

        fb = rg_times.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('eosp')
        fb.field('aor')
        fb.field('anchored')
        fb.field('anchor_up')
        fb.field('pob')
        fb.field('first_rope')
        fb.field('moored')
        fb.field('poff')
        fb.field('gangway')
        fb.field('free_p')
        fb.field('pobd')
        fb.field('last_line')
        fb.field('sailed')
        fb.field('cosp', lbl='Commenced of <br>Sea Passage',fldvalign='center')

        div_draft=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>DRAFT</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_draft.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('draft_aft_arr',placeholder='e.g. 4,5')
        fb.field('draft_fw_arr',placeholder='e.g. 4,5')
   
        div_draft=rg_details_dep.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>DRAFT</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_draft.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('draft_aft_dep',placeholder='e.g. 4,5')
        fb.field('draft_fw_dep',placeholder='e.g. 4,5')

        div_rem=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>REMAINS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_rem.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('ifo_arr',placeholder='e.g. mt.50')
        fb.field('do_arr',placeholder='e.g. mt.50')
        fb.field('lo_arr',placeholder='e.g. kgs.50')
       
        div_rem=rg_details_dep.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>REMAINS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_rem.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('ifo_dep',placeholder='e.g. mt.50')
        fb.field('do_dep',placeholder='e.g. mt.50')
        fb.field('lo_dep',placeholder='e.g. kgs.50')

        div_fw=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>FRESH WATER</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_fw.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('fw_arr',placeholder='e.g. mt.50')
 
        div_fw=rg_details_dep.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>FRESH WATER</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_fw.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('fw_dep',placeholder='e.g. mt.50')

        div_tug=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>USED TUGS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_tug.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('tug_in',placeholder='e.g. 1')
     
        div_tug=rg_details_dep.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>USED TUGS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_tug.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('tug_out',placeholder='e.g. 1')
      # fb = rg_extra.formbuilder(cols=2, border_spacing='4px',fld_width='10em')
      # fb.radioButtonText(value='^.motivo_viaggio', values='op_com:Operazioni_Commerciali,altro:Altro', lbl='Motivo Viaggio: ',validate_notnull=True,width='20em')
      # fb.radioButtonText(value='^.tipo_viaggio', values='linea:Di_Linea,occ:Occasionale', lbl='Tipo Viaggio: ',validate_notnull=True, width='20em')
      # fb.field('lavori', width='20em', colspan=2)
      # fb.field('notizie', width='20em', colspan=2)
      # fb.br()
      # fb.field('pilot_arr')
      # fb.field('pilot_arr_vhf')
      # fb.field('antifire_arr')
      # fb.field('antipol_arr')
      # fb.field('moor_arr')
      # fb.field('n_moor_arr')
      # fb.field('tug_arr')
      # fb.field('n_tug_arr')
      # fb.field('daywork')
      # fb.field('timework')
      # fb.field('pilot_dep')
      # fb.field('pilot_dep_vhf')
      # fb.field('antifire_dep')
      # fb.field('antipol_dep')
      # fb.field('moor_dep')
      # fb.field('n_moor_dep')
      # fb.field('tug_dep')
      # fb.field('n_tug_dep')

    @public_method
    def cargodocsCertLazyMode(self,pane):
        pane.stackTableHandler(relation='@cargodocs_arr',formResource='FormFromCargodocs',view_store__onBuilt=True)

    @public_method
    def usmaCertLazyMode(self,pane):
        #pane.inlineTableHandler(title='!![en]Renewal/Issue certificates',relation='@certusma_arr',viewResource='ViewFromCertusma',view_store__onBuilt=True)
        pane.stackTableHandler(relation='@certusma_arr',formResource='FormFromCertusma',view_store__onBuilt=True)
    def usmaCert2(self,bc_usma):
        rg_certusma = bc_usma.roundedGroup(title='!![en]Renewal/Issue certificates',table='shipsteps.certsanimare',region='center',datapath='.record.@certusma_arr',width='100%', height = '100%').div(margin='10px',margin_left='2px')
        fb = rg_certusma.formbuilder(cols=4, border_spacing='4px',fld_width='10em')
        fb.field('xconto',width='30em', placeholder='Es. per conto comando nave M/V...', colspan=4)  
        fb.field('docagent', placeholder="Es. Carta d'Identità")
        fb.field('doc_n')
        fb.field('issuedby', width='15em')
        fb.field('datedoc')
        fb.field('navigation', width='30em', colspan=4)
        div1=rg_certusma.div(width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb1=div1.formbuilder(colspan=3,cols=9, border_spacing='1px')
        fb1.field('sanification',lbl='')
        fb1.div('SANIFICAZIONE / ESENZIONE SANIFICAZIONE', width='30em', colspan=2)
        fb1.field('san_nsis', lbl='!![en]NSIS Code')
        fb1.br()
        fb1.field('medicines',lbl='')
        fb1.div('CASSETTA MEDICINALE / FARMACIA DI BORDO (TAB)', width='30em')
        fb1.field('tab_medicine', width='6em')
        fb1.field('med_nsis', lbl='!![en]NSIS Code')
        fb1.br()
        fb1.field('waterbox',lbl='')
        fb1.div('CASSE ACQUA POTABILE', width='30em', colspan=2)
        fb1.field('water_nsis', lbl='!![en]NSIS Code')
        fb1.br()
        fb1.field('reg_narcotics',lbl='')
        fb1.div('VIDIMAZIONE REGISTRO STUPEFACENTI', width='30em', colspan=2)
        fb1.field('narcotics_nsis', lbl='!![en]NSIS Code')
        fb1.br()
        fb1.field('newreg_narcotics',lbl='')
        fb1.div('RILASCIO E/O CHIUSURA REGISTRO STUPEFACENTI', width='30em', colspan=2)
        fb1.field('newnarcotics_nsis', lbl='!![en]NSIS Code')
        fb1.br()
        fb1.field('destroy_med',lbl='')
        fb1.div('DISTRUZIONE FARMACI STUPEFACENTI SCADUTI', width='30em', colspan=2)
        fb1.field('destroymed_nsis', lbl='!![en]NSIS Code')
        fb2=rg_certusma.formbuilder(cols=9,colspan=9, border_spacing='4px',fld_width='10em')
        fb2.field('visit_date')
        fb2.field('date')
    @public_method
    def emailArrivalLazyMode(self,pane):
        pane.inlineTableHandler(title='!![en]Email arrival',relation='@arrival_email',viewResource='ViewFromEmailArrival',view_store__onBuilt=True)

    def emailArrival(self,pane):
        pane.inlineTableHandler(title='!![en]Email arrival',relation='@arrival_email',viewResource='ViewFromEmailArrival')
   #def sof_cargo(self,pane):
   #    pane.inlineTableHandler(table='shipsteps.sof_cargo', viewResource='ViewFromSof_Cargo')
    

    def taskList(self, bc_tasklist):
        rg_prearrival = bc_tasklist.roundedGroup(title='!![en]Pre arrival',table='shipsteps.tasklist',region='left',datapath='.record.@arr_tasklist',width='550px', height = 'auto').div(margin='10px',margin_left='2px')
        rg_arrival = bc_tasklist.roundedGroup(title='!![en]Arrival/Departure',table='shipsteps.tasklist',region='center',datapath='.record.@arr_tasklist',width='520px', height = '100%', margin_left='550px').div(margin='10px',margin_left='2px')
        rg_extra = bc_tasklist.roundedGroup(title='!![en]Extra',table='shipsteps.tasklist',region='center',datapath='.record.@arr_tasklist',width='520px', height = '100%', margin_left='520px').div(margin='10px',margin_left='2px')
       
        #definizione primo rettangolo di stampa all'interno del roundedGroup Pre Arrival
        div1=rg_prearrival.div(width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb1=div1.formbuilder(colspan=3,cols=9, border_spacing='1px')

        btn_cl = fb1.Button('!![en]Print Check list',width='122px')
        btn_cl.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id',
                            nome_template = 'shipsteps.arrival:check_list', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            format_page='A4',_onResult="this.form.save();")
      #  fb1.dataController("if(msg=='check_list') SET .checklist=true", msg='^nome_temp')
        fb1.field('checklist', lbl='', margin_top='5px')
        fb1.semaphore('^.checklist', margin_top='5px')
        btn_fs = fb1.Button('!![en]Print Frontespicie', width='146px')
        btn_fs.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:front_nave',format_page='A4',_onResult="this.form.save();")
       # fb1.dataController("if(msg=='front_nave') SET .frontespizio=true", msg='^nome_temp')
        fb1.field('frontespizio', lbl='', margin_top='5px')
        fb1.semaphore('^.frontespizio', margin_top='5px')

        btn_cn = fb1.Button('!![en]Print Vessel folder', width='122px')
       #btn_cn.dataRpc(None, self.print_template,record='=#FORM.record.id',_ask=dict(title='!![en]Choose lettehead to use with this form',
       #                                        fields=[dict(name='letterhead_id', lbl='!![en]Letterhead', tag='dbSelect',columns='$id',
       #                                        hasDownArrow=True, auxColumns='$name', table='adm.htmltemplate')]), nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
       #                    nome_template = 'shipsteps.arrival:cartella_doc')
        btn_cn.dataRpc('nome_temp', self.print_template, record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:cartella_doc',format_page='A3',_onResult="this.form.save();")
       # fb1.dataController("if(msg=='cartella_doc') SET .cartella_nave=true", msg='^nome_temp')
        fb1.field('cartella_nave', lbl='', margin_top='5px')
        fb1.semaphore('^.cartella_nave', margin_top='5px')

        btn_ts = fb1.Button('!![en]Print Servicies table')
        btn_ts.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:tab_servizi',format_page='A3',_onResult="this.form.save();")
       # fb1.dataController("if(msg=='tab_servizi') SET .tab_servizi=true", msg='^nome_temp')
        fb1.field('tab_servizi', lbl='', margin_top='5px')
        fb1.semaphore('^.tab_servizi', margin_top='5px')

        btn_fc = fb1.Button('!![en]Print Cargo frontespiece')
        btn_fc.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:front_carico',format_page='A4',_onResult="this.form.save();")
       # fb1.dataController("if(msg=='front_carico') SET .front_carico=true", msg='^nome_temp')
        fb1.field('front_carico', lbl='', margin_top='5px')
        fb1.semaphore('^.front_carico', margin_top='5px')

        btn_mn = fb1.Button('!![en]Print Vessel module',action="SET .modulo_nave=true")
        btn_mn.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:mod_nave',format_page='A4',_onResult="this.form.save();")
       # fb1.dataController("if(msg=='mod_nave') SET .checklist=true", msg='^nome_temp')
        fb1.field('modulo_nave', lbl='', margin_top='5px')
        fb1.semaphore('^.modulo_nave', margin_top='5px')

        #definizione secondo rettangolo invio email all'interno del roundedGroup Pre Arrival
        div2=rg_prearrival.div('<center><strong>EMAIL</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div2.formbuilder(colspan=3,cols=9, border_spacing='2px')
        #fb = rg_prearrival.formbuilder(colspan=3,cols=6, border_spacing='4px',colswidth='10px')
       
        
        
        btn_sr = fb.Button('!![en]Shipper/Receivers')
        btn_sr.dataRpc('nome_temp', self.email_arrival_sof,
                   record='=#FORM.record.id', servizio=['arr','sof'], email_template_id='email_arr_shiprec',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the SOF and Attachments',fields=[dict(name='sof_id', lbl='!![en]sof', tag='dbSelect',columns='$id',
                             hasDownArrow=True, auxColumns='$sof_n,$ship_rec', table='shipsteps.sof',condition="$arrival_id =:cod",
                                                condition_cod='=#FORM.record.id',width='25em',validate_notnull=True),dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
        fb.field('email_ship_rec',lbl='', margin_top='5px')
        fb.semaphore('^.email_ship_rec', margin_top='5px')
        #datacontroller verifica il valore della variabile nome_temp di ritorno dalla funzione per invio email
        #e setta il valore della campo checkbox a true e lancia il messaggio 'Messaggio Creato'
      #  fb.dataController("if(msgspec=='ship_rec') {SET .email_ship_rec=true ; alert('Message created')} if(msgspec=='no_email') alert('You must insert destination email as TO or BCC'); if(msgspec=='no_sof') alert('You must select the SOF or you must create new one');", msgspec='^msg_special')
        
        btn_dog = fb.Button('!![en]Customs',width='80px')
        btn_dog.dataRpc('nome_temp', self.email_services,
                   record='=#FORM.record.id', servizio=['dogana','gdf','gdf roan'], email_template_id='email_dogana',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                    _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
        #datacontroller verifica il valore della variabile nome_temp di ritorno dalla funzione per invio email
        #e setta il valore della campo checkbox a true e lancia il messaggio 'Messaggio Creato'
       # fb.dataController("if(msgspec=='val_dog') {SET .email_dogana=true ; alert('Message created')}", msgspec='^nome_temp')
        fb.field('email_dogana',lbl='', margin_top='5px')
        fb.semaphore('^.email_dogana', margin_top='5px')

       #uploader = fb.button('Upload more files')
       #uploader.dataController("""
       #                        genro.dlg.multiUploaderDialog('!![en]Upload many files and assign them to users',{
       #                                    uploadPath:uploadPath,
       #                                    onResult:function(){
       #                                        genro.publish("floating_message",{message:"Upload completato", messageType:"message"});
       #                                        genro.publish('trigger_action',{user_id:user_id}); }
       #                                    });""",
       #                                    uploadPath=':import_queue',
       #                                    _ask=dict(title='Choose users to whom to assign files',
       #                                        fields=[dict(name='user_id', lbl='User', tag='dbselect', table='adm.user')]))
        btn_fr = fb.Button('!![en]Immigration', width='98px')
        btn_fr.dataRpc('nome_temp', self.print_template,
                   record='=#FORM.record.id', servizio=['immigration'], email_template_id='email_frontiera',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   nome_template = 'shipsteps.arrival:form_immigration', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',format_page='A4',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       # fb.dataController("if(msgspec=='val_imm') {SET .email_frontiera=true; alert('Message created')}", msgspec='^nome_temp')
        fb.field('email_frontiera',lbl='', margin_top='5px')
        fb.semaphore('^.email_frontiera', margin_top='5px')

        btn_usma = fb.Button('!![en]Sanimare',width='115px')
        btn_usma.dataRpc('nome_temp', self.email_services,
                   record='=#FORM.record.id', servizio=['sanimare'], email_template_id='email_sanimare',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       # fb.dataController("if(msgspec=='val_usma') {SET .email_usma=true ; alert('Message created')}", msgspec='^nome_temp')
        fb.field('email_usma',lbl='', margin_top='5px')
        fb.semaphore('^.email_usma', margin_top='5px')

        btn_pilot = fb.Button('!![en]Pilot/Moor',width='80px')
        btn_pilot.dataRpc('nome_temp', self.email_services,
                   record='=#FORM.record.id', servizio=['pilot','mooringmen'], email_template_id='email_pilot_moor',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       # fb.dataController("if(msgspec=='val_pil_moor') {SET .email_pilot_moor=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_pilot_moor',lbl='', margin_top='5px')
        fb.semaphore('^.email_pilot_moor', margin_top='5px')

        btn_tug = fb.Button('!![en]Tug', width='98px')
        btn_tug.dataRpc('nome_temp', self.email_services,
                   record='=#FORM.record.id', servizio=['tug'], email_template_id='email_tug',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       # fb.dataController("if(msgspec=='val_tug') {SET .email_tug=true ; alert('Message created')}", msgspec='^msg_special')
       
        fb.field('email_tug',lbl='', margin_top='5px')
        fb.semaphore('^.email_tug', margin_top='5px')

        btn_garb = fb.Button('!![en]Garbage', width='115px')
        btn_garb.dataRpc('nome_temp', self.print_template_garbage,record='=#FORM.record.id',servizio=['garbage'], email_template_id='garbage_email',
                            nome_template = 'shipsteps.garbage:garbage_request',format_page='A4',selId='=#FORM.shipsteps_garbage.view.grid.selectedId',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       
        #fb.dataController("if(msgspec=='val_garbage') {SET .email_garbage=true ; alert('Message created');} if(msgspec=='yes') alert('You must select the record as row in the garbage form'); "
        #                    , msgspec='^msg_special')
        fb.field('email_garbage',lbl='', margin_top='5px')
        fb.semaphore('^.email_garbage', margin_top='5px')
        
        btn_pfso = fb.Button('!![en]PFSO', width='80px')
        btn_pfso.dataRpc('nome_temp', self.email_services,
                   record='=#FORM.record.id', servizio=['pfso'], email_template_id='email_pfso',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       # fb.dataController("if(msgspec=='val_pfso') {SET .email_pfso=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_pfso',lbl='', margin_top='5px')
        fb.semaphore('^.email_pfso', margin_top='5px')

        btn_chem = fb.Button('!![en]Chemist', width='98px')
        btn_chem.dataRpc('nome_temp', self.email_services,
                   record='=#FORM.record.id', servizio=['chemist'], email_template_id='email_chemist',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                    _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
        #fb.dataController("if(msgspec=='val_chemist') {SET .email_chemist=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_chemist',lbl='', margin_top='5px')
        fb.semaphore('^.email_chemist', margin_top='5px')

        btn_gpg = fb.Button('!![en]GPG', width='115px')
        btn_gpg.dataRpc('nome_temp', self.email_services,
                  record='=#FORM.record.id', servizio=['gpg'], email_template_id='email_gpg',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       # fb.dataController("if(msgspec=='val_gpg') {SET .email_gpg=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_gpg',lbl='', margin_top='5px')
        fb.semaphore('^.email_gpg', margin_top='5px')

        btn_ens = fb.Button('!![en]ENS', width='80px')
        btn_ens.dataRpc('nome_temp', self.email_services,
                  record='=#FORM.record.id', servizio=['ens'], email_template_id='email_ens',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       # fb.dataController("if(msgspec=='val_ens') {SET .email_ens=true ; alert('Message created')}", msgspec='^msg_special')
       
        fb.field('email_ens',lbl='', margin_top='5px')
        fb.semaphore('^.email_ens', margin_top='5px')

        btn_ens = fb.Button('!![en]Garbage ADSP')
        btn_ens.dataRpc('nome_temp', self.email_services,
                  record='=#FORM.record.id', servizio=['adsp'], email_template_id='not_rifiuti',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',validate_notnull=True,
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
       # fb.dataController("if(msgspec=='val_adsp') {SET .email_garbage_adsp=true ; alert('Message created')}", msgspec='^msg_special')
      
        fb.field('email_garbage_adsp',lbl='', margin_top='5px')
        fb.semaphore('^.email_garbage_adsp', margin_top='5px')


       #btn_af = fb.Button('!![en]Email Antifire', width='101px')
       #fb.field('email_antifire',lbl='', margin_top='5px')
       #fb.semaphore('^.email_antifire', margin_top='5px')

        btn_update = fb.Button('!![en]services<br>updating', width='115px')
        btn_update.dataRpc('nome_temp', self.email_serv_upd,
                   record='=#FORM.record',email_template_id='email_arr_shiprec',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the services to update and Attachments',fields=[dict(name='services', lbl='!![en]Services', tag='checkboxtext',
                             table='shipsteps.services_for_email', columns='$description_serv',#values='dogana,gdf,gdf roan,pilot,mooringmen,tug,immigration,sanimare,pfso,garbage,chemist,gpg',
                             validate_notnull=True,cols=4,popup=True,colspan=2),dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        #fb.dataController("if(msgspec=='val_upd') {alert('Message created')}", msgspec='^msg_special')
        
        fb.div()
        fb.div()
     
        btn_upd_shiprec = fb.Button('!![en]Ship/Rec.<br>updating',width='80px')
        btn_upd_shiprec.dataRpc('nome_temp', self.email_arrival_sof,
                   record='=#FORM.record.id', servizio=['arr','sof'], email_template_id='email_updating_shiprec',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the SOF and Attachments',fields=[dict(name='sof_id', lbl='!![en]sof', tag='dbSelect',columns='$id',
                             hasDownArrow=True, auxColumns='$sof_n,$ship_rec', table='shipsteps.sof',condition="$arrival_id =:cod",
                                                condition_cod='=#FORM.record.id',width='25em',validate_notnull=True),dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        #datacontroller verifica il valore della variabile msg_special di ritorno dalla funzione per invio email
        #e setta il valore della campo checkbox a true e lancia il messaggio 'Messaggio Creato'
       
        #fb.dataController("if(msgspec=='ship_rec_upd') {alert('Message created')} if(msgspec=='no_email') alert('You must insert destination email as TO or BCC'); if(msgspec=='no_sof') alert('You must select the SOF or you must create new one');", msgspec='^msg_special')
        
        div3=rg_prearrival.div('<center><strong>Harbour Master - Docs before vessel arrival</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb2 = div3.formbuilder(colspan=3,cols=9, border_spacing='2px')
        btn_integr = fb2.Button('!![en]Email Alimentary integration')
        btn_integr.dataRpc('nome_temp', self.email_services,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_integrazione_alim',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
        #fb2.dataController("if(msgspec=='val_integr') {SET .email_integr=true ; alert('Message created')}", msgspec='^msg_special')
       
        fb2.field('email_integr', lbl='', margin_top='6px')
        fb2.semaphore('^.email_integr', margin_top='6px')

        btn_garb_cp = fb2.Button('!![en]Email Garbage form')
        btn_garb_cp.dataRpc('nome_temp', self.email_services,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_garbage_cp',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]),_onResult="this.form.save();")
        #fb2.dataController("if(msgspec=='val_garb_cp') {SET .email_garbage_cp=true ; alert(msg_txt)}", msgspec='^msg_special',msg_txt = 'Email ready to be sent')
       
        fb2.field('email_garbage_cp', lbl='', margin_top='6px')
        fb2.semaphore('^.email_garbage_cp', margin_top='6px')
        

        #fb.dataController("if(msgspec=='val_bulk')alert(msg_txt);",msgspec='^msg_special',msg_txt = 'Email ready to be sent')
        fb.dataController("""if(msg=='val_bulk'){alert(msg_txt);} if(msg=='val_garb_cp'){SET .email_garbage_cp=true ; alert(msg_txt);}
                             if(msg=='val_integr') {SET .email_integr=true ;genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='ship_rec_upd') genro.publish("floating_message",{message:msg_txt, messageType:"message"}); if(msg=='no_email') genro.publish("floating_message",{message:'You must insert destination email as TO or BCC', messageType:"error"}); if(msg=='no_sof') genro.publish("floating_message",{message:'You must select the SOF or you must create new one', messageType:"error"});
                             if(msg=='val_upd') genro.publish("floating_message",{message:msg_txt, messageType:"message"});
                             if(msg=='val_adsp') {SET .email_garbage_adsp=true ; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='val_ens') {SET .email_ens=true ; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='val_gpg') {SET .email_gpg=true ; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='val_chemist') {SET .email_chemist=true ; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='val_pfso') {SET .email_pfso=true ; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='val_garbage') {SET .email_garbage=true ;alert(msg_txt);} if(msg=='yes') genro.publish("floating_message",{message:'You must select the record as row in the garbage form', messageType:"error"});
                             if(msg=='val_tug') {SET .email_tug=true; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='val_pil_moor') {SET .email_pilot_moor=true; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='val_usma') {SET .email_usma=true; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='form_immigration') {SET .email_frontiera=true; alert(msg_txt);}
                             if(msg=='val_dog') {SET .email_dogana=true; genro.publish("floating_message",{message:msg_txt, messageType:"message"});}
                             if(msg=='ship_rec') {SET .email_ship_rec=true; genro.publish("floating_message",{message:msg_txt, messageType:"message"});} if(msg=='no_email') genro.publish("floating_message",{message:'You must insert destination email as TO or BCC', messageType:"error"}); if(msg=='no_sof') genro.publish("floating_message",{message:'You must select the SOF or you must create new one', messageType:"error"});
                             if(msg=='val_deroga_gb') {alert(msg_txt);}
                             if(msg=='no_moored') {genro.publish("floating_message",{message:'You must insert in arrival times date and time of vessel moored', messageType:"error"});}
                             if(msg=='mod61_arr') {alert(msg_txt);} if(msg=='nota_arr_no') genro.publish("floating_message",{message:'You must first print Nota Arrivo', messageType:"error"}); if(msg=='fal1_arr_no') genro.publish("floating_message",{message:'You must first print Fal1 arrival', messageType:"error"}); if(msg=='fal1arr_notarr') genro.publish("floating_message",{message:'You must first print Fal1 arrival and Nota Arrivo', messageType:"error"});
                             if(msg=='mod61_dep') {alert(msg_txt);} if(msg=='nota_part_no') genro.publish("floating_message",{message:'You must first print Dich. integrativa di partenza', messageType:"error"}); if(msg=='fal1_dep_no') genro.publish("floating_message",{message:'You must first print Fal1 departure', messageType:"error"}); if(msg=='fal1dep_notapart') genro.publish("floating_message",{message:'You must first print Fal1 departure and Dich. integrativa di partenza', messageType:"error"}); if(msg=='no_sailed') genro.publish("floating_message",{message:'You must first insert ets date and time', messageType:"error"});
                             if(msg=='intfat') genro.publish("floating_message",{message:msg_txt, messageType:"message"});
                             if(msg=='no_sanitation') genro.publish("floating_message",{message:'you must insert sanitation certificate in the ships docs', messageType:"error"});
                             if(msg=='mod_nave') {SET .checklist=true;}
                             if(msg=='front_carico') {SET .front_carico=true;}
                             if(msg=='tab_servizi') {SET .tab_servizi=true;}
                             if(msg=='cartella_doc') {SET .cartella_nave=true;}
                             if(msg=='front_nave') {SET .frontespizio=true;}
                             if(msg=='check_list') {SET .checklist=true;}"""
                             ,msg='^nome_temp',msg_txt = 'Email ready to be sent')

       #fb.dataController("""if(msgspec=='val_bulk'){alert(msg_txt);} if(msgspec=='val_garb_cp'){SET .email_garbage_cp=true ; alert(msg_txt);}
       #                     if(msgspec=='val_integr') {SET .email_integr=true ; alert(msg_txt);}
       #                     if(msgspec=='ship_rec_upd') {alert(msg_txt);} if(msgspec=='no_email') {alert('You must insert destination email as TO or BCC');} if(msgspec=='no_sof') {alert('You must select the SOF or you must create new one');}
       #                     if(msgspec=='val_upd') {alert(msg_txt);}
       #                     if(msgspec=='val_adsp') {SET .email_garbage_adsp=true ; alert(msg_txt);}
       #                     if(msgspec=='val_ens') {SET .email_ens=true ; alert(msg_txt);}
       #                     if(msgspec=='val_gpg') {SET .email_gpg=true ; alert(msg_txt);}
       #                     if(msgspec=='val_chemist') {SET .email_chemist=true ; alert(msg_txt);}
       #                     if(msgspec=='val_pfso') {SET .email_pfso=true ; alert(msg_txt);}
       #                     if(msgspec=='val_garbage') {SET .email_garbage=true ; alert(msg_txt);} if(msgspec=='yes') {alert('You must select the record as row in the garbage form');}
       #                     if(msgspec=='val_tug') {SET .email_tug=true ; alert(msg_txt);}
       #                     if(msgspec=='val_pil_moor') {SET .email_pilot_moor=true ; alert(msg_txt);}
       #                     if(msgspec=='val_usma') {SET .email_usma=true ; alert(msg_txt);}
       #                     if(msgspec=='val_imm') {SET .email_frontiera=true; alert(msg_txt);}
       #                     if(msgspec=='val_dog') {SET .email_dogana=true ; alert(msg_txt);}
       #                     if(msgspec=='ship_rec') {SET .email_ship_rec=true ; alert(msg_txt);} if(msgspec=='no_email') {alert('You must insert destination email as TO or BCC');} if(msgspec=='no_sof') {alert('You must select the SOF or you must create new one');}
       #                     if(msg=='mod61_arr') {alert(msg_txt);} if(msg=='nota_arr_no') {alert('You must first print Nota Arrivo');} if(msg=='fal1_arr_no') {alert('You must first print Fal1 arrival');} if(msg=='fal1arr_notarr') {alert('You must first print Fal1 arrival and Nota Arrivo');}
       #                     if(msg=='mod61_dep') {alert(msg_txt);} if(msg=='nota_part_no') {alert('You must first print Dich. integrativa di partenza');} if(msg=='fal1_dep_no') {alert('You must first print Fal1 departure');} if(msg=='fal1dep_notapart') {alert('You must first print Fal1 departure and Dich. integrativa di partenza');} if(msg=='no_sailed') {alert('You must first insert ets date and time');}
       #                     if(msg=='intfat') genro.publish("floating_message",{message:"email ready to be sent", messageType:"message"});
       #                     if(msg=='mod_nave') {SET .checklist=true;}
       #                     if(msg=='front_carico') {SET .front_carico=true;}
       #                     if(msg=='tab_servizi') {SET .tab_servizi=true;}
       #                     if(msg=='cartella_doc') {SET .cartella_nave=true;}
       #                     if(msg=='front_nave') {SET .frontespizio=true;}
       #                     if(msg=='check_list') {SET .checklist=true;}""",msgspec='^msg_special', msg='^nome_temp',msg_txt = 'Email ready to be sent')

        
        div_arr=rg_arrival.div('<center><strong>ARRIVAL</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb_arr=div_arr.formbuilder(colspan=2,cols=4, border_spacing='1px')
        btn_fgdf_cp = fb_arr.Button('!![en]Form GdF')
        btn_fgdf_cp.dataRpc('', self.print_template,record='=#FORM.record.id',
                            nome_template = 'shipsteps.arrival:form_gdf', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',format_page='A4')
        btn_fimm_cp = fb_arr.Button('!![en]Form Immigration')
        btn_fimm_cp.dataRpc('', self.print_template,record='=#FORM.record.id', nome_template = 'shipsteps.arrival:form_immigration', 
                                         nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',format_page='A4', only_print='yes')
        btn_fprov_cp = fb_arr.Button('!![en]Form Provisions')
        btn_fprov_cp.dataRpc('', self.print_template,record='=#FORM.record.id',
                            nome_template = 'shipsteps.arrival:form_provisions', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',format_page='A4')
        fb_arr.br()
        
        btn_fsan = fb_arr.Button('!![en]Dichiarazione Sanimare')
        btn_fsan.dataRpc('nome_temp', self.apridoc,record='=#FORM.record',nome_form='DichSanimare', _virtual_column='lastport,nextport,vesselname,flag,imo,tsl')
        btn_intfiore = fb_arr.Button('!![en]CheckList Fiore')
        btn_intfiore.dataRpc('', self.apridoc,record='=#FORM.record',nome_form='InterferenzeFiore', _virtual_column='lastport,nextport,vesselname,flag,imo,tsl')
        fb_arr.br()
        btn_chim_cp = fb_arr.Button('!![en]Email Cert. Chimico CP')
        btn_chim_cp.dataRpc('nome_temp', self.email_services,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_chimico_cp',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',validate_notnull=True,
                             cols=4,popup=True,colspan=2)]))
        btn_chim_cp = fb_arr.Button('!![en]Email Waste derogation CP')
        btn_chim_cp.dataRpc('nome_temp', self.print_template_derogagb,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_deroga_garbage',
                            nome_template = 'shipsteps.arrival:deroga_rifiuti',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                            moored='=#FORM.record.@time_arr.moored',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',validate_notnull=True,
                             cols=4,popup=True,colspan=2)]))
        div_dep=rg_arrival.div('<center><strong>DEPARTURE</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb_dep=div_dep.formbuilder(colspan=2,cols=4, border_spacing='1px')
        fb_dep.Button('!![en]Vessel services', action="""{SET shipsteps_arrival.form.pippo='services';}""")
        fb_dep.Button('!![en]GdF Departure',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.arrival",
                                                                               res_type:'print',
                                                                               resource:'Partenza_Finanza',
                                                                               pkey: pkey})""",
                                                                               pkey='=#FORM.pkey')
        div_extra=rg_arrival.div('<center><strong>EXTRA NSW FORMS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb_extra=div_extra.formbuilder(colspan=2,cols=4, border_spacing='1px')
        btn_accosto=fb_extra.Button('!![en]Email Domanda Accosto',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.arrival",
                                                                               res_type:'print',
                                                                               resource:'Accosto',
                                                                               pkey: pkey});""",
                                                                               pkey='=#FORM.pkey')

        btn_cambio_accosto=fb_extra.Button('!![en]Email Cambio Accosto',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.arrival",
                                                                               res_type:'print',
                                                                               resource:'Cambio_accosto',
                                                                               pkey: pkey});""",
                                                                               pkey='=#FORM.pkey')
        btn_com_partenza=fb_extra.Button('!![en]Email Comunicazione Partenza',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.arrival",
                                                                               res_type:'print',
                                                                               resource:'Partenza',
                                                                               pkey: pkey});""",
                                                                               pkey='=#FORM.pkey')
        fb_extra.br()
        btn_fal1_arr=fb_extra.Button('!![en]Fal1 Arrival',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.arrival",
                                                                               res_type:'print',
                                                                               resource:'general_decl',
                                                                               pkey: pkey});""",
                                                                               pkey='=#FORM.pkey')
        btn_nota_arr=fb_extra.Button('Nota Arrivo',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.arrival",
                                                                               res_type:'print',
                                                                               resource:'nota_arrivo',
                                                                               pkey: pkey});""",
                                                                               pkey='=#FORM.pkey')
        btn_arrivo = fb_extra.Button('!![en]Email arrival', width='115px')
        btn_arrivo.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id',servizio=['capitaneria_nsw'], email_template_id='email_arrivo_cp',
                            nome_template = 'shipsteps.arrival:mod61_arr',format_page='A4',nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb_extra.br()
        btn_fal1_dep=fb_extra.Button('!![en]Fal1 Departure',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.arrival",
                                                                               res_type:'print',
                                                                               resource:'general_decl_dep',
                                                                               pkey: pkey});""",
                                                                               pkey='=#FORM.pkey')
        btn_nota_dep=fb_extra.Button('Dich.Intergr.Partenza',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.arrival",
                                                                               res_type:'print',
                                                                               resource:'dichiarazione_partenza',
                                                                               pkey: pkey});""",
                                                                               pkey='=#FORM.pkey')
        btn_departure = fb_extra.Button('!![en]Email Departure', width='115px')
        btn_departure.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id',servizio=['capitaneria_nsw'], email_template_id='email_partenza_cp',
                            nome_template = 'shipsteps.arrival:mod61_dep',format_page='A4',nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))

        #fb_extra.dataController("""genro.publish("floating_message",{message:'prova'), messageType:"message"}""")
       #genro.publish("floating_message",{message:"Email ready to be sent", messageType:"message"});

        div_extra=rg_extra.div('<center><strong>EXTRA</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb_extra=div_extra.formbuilder(colspan=2,cols=4, border_spacing='1px')
        #btn_intfat = fb_extra.Button('!![en]Intestazione Fatt', width='115px')
        #btn_intfat.dataRpc('nome_temp', self.email_intfat,record='=#FORM.record',nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome')

        dlg = rg_extra.dialog(nodeId='mydialog',style='width:600px;height:150px;',title='Intestazione fattura',closable=True)
        dlg.span('Intestazione fatt: ')
        
        dlg.span().simpleTextArea(value='^intfat', width='40em', height='50px')
        dlg.hr()
        btn_dlg=dlg.button('Visualizza Intestazione')
        btn_dlg1=dlg.button('Email Intestazione fattura')
        
        btn_dlg1.dataRpc('nome_temp', self.email_intfat,record='=#FORM.record',nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome')
        fb_extra.button('Intestazione Fatt', action="genro.wdgById('mydialog').show()")
        btn_dlg.dataRpc('intfat',self.intfat,record='=#FORM.record')
        
        dlgws = rg_extra.dialog(nodeId='dialog_ws',style='width:300px;height:100px;',title='Water supply',closable=True)
        dlgws.span('Quantity mt.: ')
        dlgws.span().textbox(value='^.acqua',table='shipsteps.arrival', columns='$acqua', width='10em')
        dlgws.hr()
        btn_dlgws=dlgws.button('Email request ws')
        btn_dlgws.dataRpc('nome_temp', self.email_ws,record='=#FORM.record',servizio=['ws'], email_template_id='email_water_supply',
                            nome_template = 'shipsteps.arrival:water_supply',nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            _onResult="""if(result=='no_int'){genro.publish('floating_message',{message:"manca l'intestazione: inseriscila",messageType:'error',duration_out:6});}
                                         if(result=='ws')genro.publish("floating_message",{message:"email ready to be sent", messageType:"message"});this.form.save();""")#this.form.save();
                                         #this.form.reload()""")
        fb_extra.button('Water supply', action="genro.wdgById('dialog_ws').show()")
    
    
    @public_method
    def intfat(self,record, **kwargs):  
        intfat_id = record['invoice_det_id']
        tbl_invoice = self.db.table('shipsteps.invoice_det')
        int_fat = tbl_invoice.readColumns(columns="""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'') || coalesce(' - Vat: ' || $vat,'') || 
                                     coalesce(' - unique code: ' || $cod_univoco,'') || coalesce(' - pec: ' || $pec,'') AS rag_soc""", where='$id=:id_inv',id_inv=intfat_id)
        return int_fat

    def allegatiArrivo(self,pane):
        pane.attachmentGrid(viewResource='ViewFromArrivalAtc')

    @public_method
    def shorePassLazyMode(self,pane):
        pane.stackTableHandler(relation='@shorepass_arr',formResource='Form',view_store__onBuilt=True)


    def shorepass(self, pane):
        pane.stackTableHandler(relation='@shorepass_arr',formResource='Form')

    def garbage(self, pane):
        pane.inlineTableHandler(relation='@garbage_arr',viewResource='ViewFromGarbage')

    @public_method
    def rinfusaLazyMode(self,pane):
        pane.stackTableHandler(relation='@rinfusa_arr',formResource='FormFromRinfusa',view_store__onBuilt=True)

    def rinfusa(self, pane):
        pane.stackTableHandler(relation='@rinfusa_arr',formResource='FormFromRinfusa')
    
    @public_method
    def bunkerLazyMode(self,pane):
        pane.stackTableHandler(relation='@bunker_arr',formResource='FormFromBunker',view_store__onBuilt=True)

    def bunker(self, pane):   
        pane.stackTableHandler(relation='@bunker_arr',formResource='FormFromBunker')

    @public_method
    def email_services(self,record,email_template_id=None,servizio=[],nome_temp=None,**kwargs):
    #def email_services(self, record,email_template_id=None,servizio=[],selPkeys_att=None,**kwargs):
    
        #creiamo la variabile lista attcmt dove tramite il ciclo for andremo a sostituire la parola 'site' con '/home'
        attcmt=[]
        
        #se il servizio è mod61_arr appendiamo agli attachments il fal1_arr e la nota_arrivo e il mod61
        if nome_temp == 'mod61_arr':
            attcmt.append(self.fal1_path)
            attcmt.append(self.notacp_path)
            file_path_mod61 = 'site:stampe_template/mod61_arr_'+self.vessel_name+'.pdf'
            fileSn_mod61 = self.site.storageNode(file_path_mod61)
            attcmt.append(fileSn_mod61.internal_path)
        #se il servizio è mod61_dep appendiamo agli attachments il fal1_dep e la dichiarazione integrativa di partenza e il mod61
        if nome_temp == 'mod61_dep':
            attcmt.append(self.fal1_path)
            attcmt.append(self.notacp_path)
            file_path_mod61 = 'site:stampe_template/mod61_dep_'+self.vessel_name+'.pdf'
            fileSn_mod61 = self.site.storageNode(file_path_mod61)
            attcmt.append(fileSn_mod61.internal_path)
        #se il servizio è form_immigration appendiamo agli attachments il form immigration
        if nome_temp == 'form_immigration':
            file_path_imm = 'site:stampe_template/form_immigration.pdf'
            fileSn_imm = self.site.storageNode(file_path_imm)
            attcmt.append(fileSn_imm.internal_path)    
        #trasformiamo la stringa pkeys allegati in una lista prelevandoli dai kwargs ricevuti tramite bottone
        #ma verifichiamo se nei kwargs gli allegati ci sono per non ritrovarci la variabile lista_all senza assegnazione
        
        for chiavi in kwargs.keys():
            if chiavi=='allegati':
                if kwargs['allegati']:
                    lista_all=list(kwargs['allegati'].split(","))
                else:
                    lista_all=None
       #if kwargs['allegati']:
       #    lista_all=list(kwargs['allegati'].split(","))
       #else:
       #    lista_all=None
        
        #lettura degli attachment
        if lista_all:
            len_allegati = len(lista_all) #verifichiamo la lunghezza della lista pkeys tabella allegati
            file_url=[]
            tbl_att =  self.db.table('shipsteps.arrival_atc') #definiamo la variabile della tabella allegati
            #ciclo for per la lettura dei dati sulla tabella allegati ritornando su ogni ciclo tramite la pkey dell'allegato la colonna $fileurl e alla fine
            #viene appesa alla variabile lista file_url
            for e in range(len_allegati):
                pkeys_att=lista_all[e]
                fileurl = tbl_att.readColumns(columns='$fileurl',
                      where='$id=:att_id',
                        att_id=pkeys_att)
                if fileurl is not None and fileurl !='':
                    file_url.append(fileurl)
        
            ln = len(file_url)
            for r in range(ln):
                fileurl = file_url[r]
                file_path = fileurl.replace('/home','site')
                fileSn = self.site.storageNode(file_path)
                attcmt.append(fileSn.internal_path)
       
        #lettura degli attachment in email_service_atc
        #verifichiamo il numero di servizi
        ln_serv=len(servizio)
        #definiamo le tabelle su cui effettuare le ricerche
        tbl_emailservices = self.db.table('shipsteps.email_services')
        tbl_emailserv_atc = self.db.table('shipsteps.email_services_atc')
        #leggiamo prima gli id dei servizi su email_services così passiamo gli id alla tabella di attachment per la lettura dell'url
        #per poi trasformarlo nel giusto path che appendiamo agli attachment dell'email
        for e in range(ln_serv):
            serv=servizio[e]
            service_id = tbl_emailservices.readColumns(columns="$id", where='$service_for_email=:serv', serv=serv)
        
        
            att_services = tbl_emailserv_atc.query(columns="$filepath", where='$maintable_id=:m_id' ,
                                                                    m_id=service_id).fetch()
            if att_services	!= []:
                file_url = att_services[e][0]
                file_path = file_url.replace('/home','site')
                fileSn = self.site.storageNode(file_path)
                attcmt.append(fileSn.internal_path)
          
        #vecchio codice con rilevamento attachments tramite casella checkbox
       #if not record:
       #    return
       #tbl_att =  self.db.table('shipsteps.arrival_atc')
       #fileurl = tbl_att.query(columns='$fileurl',
       #          where='$att_email=:a_att AND $maintable_id=:mt_id',
       #            a_att='true',mt_id=record).fetch()
      
       #ln = len(fileurl)
       #attcmt=[]
       #for r in range(ln):
       #    file_url = fileurl[r][0]
       #    file_path = file_url.replace('/home','site')
       #    fileSn = self.site.storageNode(file_path)
       #    attcmt.append(fileSn.internal_path)

        #Condizioniamo l'aggiunta dell'allegato se il servizio invio email è il garbage
        if servizio==['garbage']:
            file_path_gb = 'site:stampe_template/garbage_request.pdf'
            fileSn_gb = self.site.storageNode(file_path_gb)
            attcmt.append(fileSn_gb.internal_path)
        #Condizioniamo l'aggiunta dell'allegato se il servizio invio email è la deroga rifiuti
        if email_template_id == 'email_deroga_garbage':
            file_path_gb = 'site:stampe_template/deroga_rifiuti.pdf'
            fileSn_gb = self.site.storageNode(file_path_gb)
            attcmt.append(fileSn_gb.internal_path)    
           #if r < (ln-1):
           #    attcmt = attcmt + fileSn.internal_path + ','
           #else:
           #    attcmt = attcmt + fileSn.internal_path

        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('shipsteps.staff')
        account_email = tbl_staff.readColumns(columns='$email_account_id',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('shipsteps.agency')
        account_emailpec = tbl_agency.readColumns(columns='$emailpec_account_id',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

      
        #Lettura degli indirizzi email destinatari
        ln_serv=len(servizio)

        #email_d, email_cc_d, email_pec_d, email_pec_cc_d=[],[],[],[]
        email_d, email_cc_d,email_bcc_d, email_pec_d, email_pec_cc_d='','','','',''
        tbl_email_services=self.db.table('shipsteps.email_services')
        for e in range(ln_serv):
            serv=servizio[e]

            email_dest, email_cc_dest,email_bcc_dest, email_pec_dest, email_pec_cc_dest = tbl_email_services.readColumns(columns="""$email,$email_cc,$email_bcc,$email_pec,$email_cc_pec""",
                                                    where='$service_for_email=:serv AND $agency_id=:ag_id', serv=serv,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'))
            #email_d.append(email_dest)
            #email_cc_d.append(email_cc_dest)
            #email_pec_d.append(email_pec_dest)
            #email_pec_cc_d.append(email_pec_cc_dest)

            if e < (ln_serv-1):
                if email_dest is not None:
                    email_d = email_d + email_dest + ','
                if email_cc_dest is not None:
                    email_cc_d = email_cc_d + email_cc_dest + ','
                if email_bcc_dest is not None:
                    email_bcc_d = email_bcc_d + email_bcc_dest + ','
                if email_pec_dest is not None:
                    email_pec_d = email_pec_d + email_pec_dest + ','
                if email_pec_cc_dest is not None:
                    email_pec_cc_d = email_pec_cc_d + email_pec_cc_dest + ','
            else:
                if email_dest is not None:
                    email_d = email_d + email_dest
                if email_cc_dest is not None:
                    email_cc_d = email_cc_d + email_cc_dest
                if email_bcc_dest is not None:
                    email_bcc_d = email_bcc_d + email_bcc_dest
                if email_pec_dest is not None:
                    email_pec_d = email_pec_d + email_pec_dest
                if email_pec_cc_dest is not None:
                    email_pec_cc_d = email_pec_cc_d + email_pec_cc_dest
        
        if (email_dest) is not None:
            self.db.table('email.message').newMessageFromUserTemplate(
                                                          record_id=record,
                                                          table='shipsteps.arrival',
                                                          account_id = account_email,
                                                          to_address=email_d,
                                                          cc_address=email_cc_d,
                                                          bcc_address=email_bcc_d,
                                                          attachments=attcmt,
                                                          template_code=email_template_id)
            #print(x)
            self.db.commit()

        if (email_pec_dest) is not None:
            self.db.table('email.message').newMessageFromUserTemplate(
                                                          record_id=record,
                                                          table='shipsteps.arrival',
                                                          account_id = account_emailpec,
                                                          to_address=email_pec_d,
                                                          cc_address=email_pec_cc_d,
                                                          attachments=attcmt,
                                                          template_code=email_template_id)
            self.db.commit()
        
        
        if (email_dest or email_pec_dest) is not None:

            if email_template_id == 'email_dogana':
                nome_temp = 'val_dog'
            elif email_template_id == 'email_frontiera':
                nome_temp = 'val_imm'
            elif email_template_id == 'email_sanimare':
                nome_temp = 'val_usma'
            elif email_template_id == 'email_pfso':
                nome_temp = 'val_pfso'
            elif email_template_id == 'email_pilot_moor':
                nome_temp = 'val_pil_moor'
            elif email_template_id == 'email_tug':
                nome_temp = 'val_tug'
            elif email_template_id == 'garbage_email':
                nome_temp = 'val_garbage'
            elif email_template_id == 'email_chemist':
                nome_temp = 'val_chemist'
            elif email_template_id == 'email_gpg':
                nome_temp = 'val_gpg'
            elif email_template_id == 'email_ens':
                nome_temp = 'val_ens'
            elif email_template_id == 'email_garbage_cp':
                nome_temp = 'val_garb_cp'
            elif email_template_id == 'email_integrazione_alim':
                nome_temp = 'val_integr'
            elif email_template_id == 'email_chimico_cp':
                nome_temp = 'ship_rec'
            elif email_template_id == 'not_rifiuti':
                nome_temp = 'val_adsp'
            elif email_template_id == 'email_arrivo_cp':
                nome_temp = 'val_mod61arr'
            elif email_template_id == 'email_partenza_cp':
                nome_temp = 'val_mod61dep'
            elif email_template_id == 'email_water_supply':
                nome_temp = 'val_ws'
            elif email_template_id == 'email_deroga_garbage':
                nome_temp = 'val_deroga_gb'    
            return nome_temp
    
    @public_method
    def email_serv_upd(self, record,email_template_id=None,selPkeys_att=None, **kwargs):
        
        if not record:
            return
        #lettura del record_id della tabella arrival
        record_id=record['id']
        #lettura dati su tabella arrival
        tbl_arrival = self.db.table('shipsteps.arrival')
        vessel_type,vessel_name,eta_arr,info_moor = tbl_arrival.readColumns(columns='@vessel_details_id.@imbarcazione_id.tipo,@vessel_details_id.@imbarcazione_id.nome,$eta,$info_moor',
                  where='$agency_id=:ag_id AND $id=:rec_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'),rec_id=record_id)
        eta = eta_arr.strftime("%d/%m/%Y, %H:%M")    
        
        #creiamo la variabile lista attcmt dove tramite il ciclo for andremo a sostituire la parola 'site' con '/home'
        attcmt=[]
        
        #verifichiamo che nei kwargs['allegati'] non abbiamo il valore nullo e trasformiamo la stringa pkeys allegati in una lista prelevandoli dai kwargs ricevuti tramite bottone
        if kwargs['allegati'] is not None:
            lista_all = list(kwargs['allegati'].split(","))
        else:
            lista_all = None
        
        #lettura degli attachment
        if lista_all is not None:
            len_allegati = len(lista_all) #verifichiamo la lunghezza della lista pkeys tabella allegati
            file_url=[]
            tbl_att =  self.db.table('shipsteps.arrival_atc') #definiamo la variabile della tabella allegati
            #ciclo for per la lettura dei dati sulla tabella allegati ritornando su ogni ciclo tramite la pkey dell'allegato la colonna $fileurl e alla fine
            #viene appesa alla variabile lista file_url
            for e in range(len_allegati):
                pkeys_att=lista_all[e]
                fileurl = tbl_att.readColumns(columns='$fileurl',
                      where='$id=:att_id',
                        att_id=pkeys_att)
                if fileurl is not None and fileurl !='':
                    file_url.append(fileurl)
        
            ln = len(file_url)
            for r in range(ln):
                fileurl = file_url[r]
                file_path = fileurl.replace('/home','site')
                fileSn = self.site.storageNode(file_path)
                attcmt.append(fileSn.internal_path)

        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('shipsteps.staff')
        account_email,email_mittente,user_fullname = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,$fullname',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('shipsteps.agency')
        agency_name,ag_fullstyle,account_emailpec,emailpec_mitt = tbl_agency.readColumns(columns='$agency_name,$fullstyle,$emailpec_account_id, @emailpec_account_id.address',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        #preleviamo dai kwargs i servizi per gli aggiornamenti
        services=kwargs['services']
        #trasformiamo la stringa services in una lista
        servizio=list(services.split(","))
        #troviamo la lunghezza della variabile servizio
        #print(x)
        ln_serv=len(servizio)
        #assegnamo le varibili liste per inserire successivamente i risultati della ricerca sulla tabella email_services
        destinatario,destinatario_pec,email_d, email_cc_d,email_bcc_d, email_pec_d, email_pec_cc_d=[],[],[],[],[],[],[]
        #definiamo la variabile contentente la tabella email_services
        tbl_email_services=self.db.table('shipsteps.email_services')
        #con il ciclo for ad ogni passaggio otteniamo il nome del servizio che passeremo alla query e i risultati saranno appesi alle liste
        for e in range(ln_serv):
            serv=servizio[e]

            dest,email_dest, email_cc_dest,email_bcc_dest = tbl_email_services.readColumns(columns="""$consignee,$email,$email_cc,$email_bcc""",
                                                    where="$service_for_email_id=:serv AND $agency_id=:ag_id", serv=serv,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'))
            dest_pec,email_pec_dest, email_pec_cc_dest = tbl_email_services.readColumns(columns="""$consignee,$email_pec,$email_cc_pec""",
                                                    where='$service_for_email_id=:serv AND $agency_id=:ag_id AND $email_pec IS NOT NULL', serv=serv,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'))
            if dest is not None and dest !='':
                destinatario.append('a: ' + dest)
            if dest_pec is not None and dest_pec !='':
                destinatario_pec.append('a: ' + dest_pec)
            if email_dest is not None and email_dest !='':
                email_d.append(email_dest)
            if email_cc_dest is not None and email_cc_dest != '':
                email_cc_d.append(email_cc_dest)
            if email_bcc_dest is not None and email_bcc_dest != '':    
                email_bcc_d.append(email_bcc_dest)
            if email_pec_dest is not None and email_pec_dest != '':
                email_pec_d.append(email_pec_dest)
            if email_pec_cc_dest is not None and email_pec_cc_dest !='':
                email_pec_cc_d.append(email_pec_cc_dest)
        #trasformiamo le liste in stringhe assegnandole alle relative variabili
        consignee='<br>'.join([str(item) for item in destinatario])
        consignee_pec='<br>'.join([str(item) for item in destinatario_pec])
        email_to = ','.join([str(item) for item in email_d])
        email_cc = ','.join([str(item) for item in email_cc_d])
        email_bcc = ','.join([str(item) for item in email_bcc_d])
        email_pec = ','.join([str(item) for item in email_pec_d])
        email_pec_cc = ','.join([str(item) for item in email_pec_cc_d])
        
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")    
        if cur_time < '13:00:00':
            sal='Buongiorno,'  
        elif cur_time < '17:00:00':
            sal='Buon pomeriggio'
        elif cur_time < '24:00:00':
            sal = 'Buonasera,' 
        elif cur_time < '04:00:00':
            sal = 'Buona notte,'      

        subject='aggiornamento '+vessel_type + ' ' + vessel_name + ' ref:' + record['reference_num']
        body_header="""<span style="font-family:courier new,courier,monospace;">""" + 'da: '+ agency_name + '<br>' + consignee + '<br><br>'
        body_header_pec="""<span style="font-family:courier new,courier,monospace;">""" + 'da: '+ agency_name + '<br>' + consignee_pec + '<br><br>'
        body_footer= 'Cordiali saluti<br><br>' + user_fullname + '<br><br>' + ag_fullstyle + """</span></div>"""
        if info_moor is None:
            info_moor=''
        body_msg=(sal + '<br>' + "con la presente si comunica che il nuovo ETA della " +vessel_type + ' ' + vessel_name + " è il " + eta + '<br><br>' + info_moor)
        body_html=(body_header + body_msg + body_footer )
        #print(x)
        if email_to:
            self.db.table('email.message').newMessage(account_id=account_email,
                           to_address=email_to,
                           from_address=email_mittente,
                           subject=subject, body=body_html, 
                           cc_address=email_cc, 
                           bcc_address=email_bcc, attachments=attcmt,
                           html=True)
            self.db.commit()
        body_html_pec=(body_header_pec + body_msg + body_footer )
        if email_pec is not None and email_pec!='':
            
            self.db.table('email.message').newMessage(account_id=account_emailpec,
                           to_address=email_pec,
                           from_address=emailpec_mitt,
                           subject=subject, body=body_html_pec, 
                           cc_address=email_pec_cc, 
                           attachments=attcmt,
                           html=True)
            self.db.commit()
        if (email_dest or email_pec_dest) is not None:
            nome_temp='val_upd'
            return nome_temp
       # print(x)

    @public_method
    def email_intfat(self, record, **kwargs):
        
        if not record:
            return
        #lettura del record_id della tabella arrival
        record_id=record['id']
        vessel_type = record['@vessel_details_id.@imbarcazione_id.tipo']
        vessel_name = record['@vessel_details_id.@imbarcazione_id.nome']
        intfat_id = record['invoice_det_id']
        tbl_invoice = self.db.table('shipsteps.invoice_det')
        int_fat = tbl_invoice.readColumns(columns="""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'') || coalesce(' - Vat: ' || $vat,'') || 
                                     coalesce(' - unique code: ' || $cod_univoco,'') || coalesce(' - pec: ' || $pec,'') AS rag_soc""", where='$id=:id_inv',id_inv=intfat_id)
        #rag_soc,indirizzo,cap,citta,vat,cf,cod_un,pec = tbl_invoice.readColumns(columns='$rag_sociale,$address,$cap,$city,$vat,$cf,$cod_univoco,$pec', where='$id=:id_inv',id_inv=intfat_id)
        if int_fat == [None, None, None, None, None, None, None]:
            nome_temp='no_int'
            return nome_temp
        
        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('shipsteps.staff')
        account_email,email_mittente,user_fullname = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,$fullname',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('shipsteps.agency')
        agency_name,ag_fullstyle,account_emailpec,emailpec_mitt = tbl_agency.readColumns(columns='$agency_name,$fullstyle,$emailpec_account_id, @emailpec_account_id.address',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        
        
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")    
        if cur_time < '13:00:00':
            sal='Buongiorno,'  
        elif cur_time < '17:00:00':
            sal='Buon pomeriggio'
        elif cur_time < '24:00:00':
            sal = 'Buonasera,' 
        elif cur_time < '04:00:00':
            sal = 'Buona notte,'      
       
        subject='Intestazione fatture '+vessel_type + ' ' + vessel_name + ' ref:' + record['reference_num']
        #body_header="""<span style="font-family:courier new,courier,monospace;">""" + 'da: '+ agency_name + '<br>' + consignee + '<br><br>'
        body_footer= 'Cordiali saluti<br><br>' + user_fullname + '<br><br>' + ag_fullstyle + """</span></div>"""
        
        body_msg=("""<span style="font-family:courier new,courier,monospace;">""" + sal + '<br>' + "con la presente siamo a girarVi intestazione fatture per " +vessel_type + ' ' + vessel_name + " :" + '<br><br>' +
                        int_fat + '<br><br>')
        body_html=(body_msg + body_footer )
        #print(x)
        
        self.db.table('email.message').newMessage(account_id=account_email,
                           to_address='',
                           from_address=email_mittente,
                           subject=subject, body=body_html, 
                           cc_address='',
                           html=True)
        self.db.commit()
        
        nome_temp='intfat'
        return nome_temp

    @public_method
    def email_ws(self, record, **kwargs):
        result = Bag()
        if not record:
            return
        #lettura del record_id della tabella arrival
        record_id=record['id']
        vessel_type = record['@vessel_details_id.@imbarcazione_id.tipo']
        vessel_name = record['@vessel_details_id.@imbarcazione_id.nome']
        intfat_id = record['invoice_det_id']
        qt_ws = record['@arr_tasklist.acqua']
        tbl_invoice = self.db.table('shipsteps.invoice_det')
        int_fat = tbl_invoice.readColumns(columns="""$rag_sociale ||' '|| coalesce($address, '') ||' '|| coalesce($cap,'') ||' '|| coalesce($city,'') || coalesce(' Vat: ' || $vat,'') || 
                                     coalesce(' unique code: ' || $cod_univoco,'') || coalesce(' pec: ' || $pec,'') AS rag_soc""", where='$id=:id_inv',id_inv=intfat_id)
        #rag_soc,indirizzo,cap,citta,vat,cf,cod_un,pec = tbl_invoice.readColumns(columns='$rag_sociale,$address,$cap,$city,$vat,$cf,$cod_univoco,$pec', where='$id=:id_inv',id_inv=intfat_id)
        if int_fat == [None, None, None, None, None, None, None]:
            nome_temp='no_int'
            result['int'] = 'no'
           
            return nome_temp
        
        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('shipsteps.staff')
        account_email,email_mittente,user_fullname = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,$fullname',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('shipsteps.agency')
        agency_name,ag_fullstyle,account_emailpec,emailpec_mitt = tbl_agency.readColumns(columns='$agency_name,$fullstyle,$emailpec_account_id, @emailpec_account_id.address',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        #preleviamo dai kwargs i servizi per gli aggiornamenti
        servizio=kwargs['servizio']
        #trasformiamo la stringa services in una lista
        #servizio=list(services.split(","))
        #troviamo la lunghezza della variabile servizio
        #print(x)
        ln_serv=len(servizio)
        #assegnamo le varibili liste per inserire successivamente i risultati della ricerca sulla tabella email_services
        destinatario,destinatario_pec,email_d, email_cc_d,email_bcc_d, email_pec_d, email_pec_cc_d=[],[],[],[],[],[],[]
        #definiamo la variabile contentente la tabella email_services
        tbl_email_services=self.db.table('shipsteps.email_services')
        #con il ciclo for ad ogni passaggio otteniamo il nome del servizio che passeremo alla query e i risultati saranno appesi alle liste
        for e in range(ln_serv):
            serv=servizio[e]

            dest,email_dest, email_cc_dest,email_bcc_dest = tbl_email_services.readColumns(columns="""$consignee,$email,$email_cc,$email_bcc""",
                                                    where="$service_for_email_id=:serv AND $agency_id=:ag_id", serv=serv,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'))
            dest_pec,email_pec_dest, email_pec_cc_dest = tbl_email_services.readColumns(columns="""$consignee,$email_pec,$email_cc_pec""",
                                                    where='$service_for_email_id=:serv AND $agency_id=:ag_id AND $email_pec IS NOT NULL', serv=serv,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'))
            if dest is not None and dest !='':
                destinatario.append('a: ' + dest)
            if dest_pec is not None and dest_pec !='':
                destinatario_pec.append('a: ' + dest_pec)
            if email_dest is not None and email_dest !='':
                email_d.append(email_dest)
            if email_cc_dest is not None and email_cc_dest != '':
                email_cc_d.append(email_cc_dest)
            if email_bcc_dest is not None and email_bcc_dest != '':    
                email_bcc_d.append(email_bcc_dest)
            if email_pec_dest is not None and email_pec_dest != '':
                email_pec_d.append(email_pec_dest)
            if email_pec_cc_dest is not None and email_pec_cc_dest !='':
                email_pec_cc_d.append(email_pec_cc_dest)
        #trasformiamo le liste in stringhe assegnandole alle relative variabili
        consignee='<br>'.join([str(item) for item in destinatario])
        consignee_pec='<br>'.join([str(item) for item in destinatario_pec])
        email_to = ','.join([str(item) for item in email_d])
        email_cc = ','.join([str(item) for item in email_cc_d])
        email_bcc = ','.join([str(item) for item in email_bcc_d])
        email_pec = ','.join([str(item) for item in email_pec_d])
        email_pec_cc = ','.join([str(item) for item in email_pec_cc_d])
        
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")    
        if cur_time < '13:00:00':
            sal='Buongiorno,'  
        elif cur_time < '17:00:00':
            sal='Buon pomeriggio'
        elif cur_time < '24:00:00':
            sal = 'Buonasera,' 
        elif cur_time < '04:00:00':
            sal = 'Buona notte,'      
        
        subject='Richiesta fornitura acqua '+vessel_type + ' ' + vessel_name + ' ref:' + record['reference_num']
        #body_header="""<span style="font-family:courier new,courier,monospace;">""" + 'da: '+ agency_name + '<br>' + consignee + '<br><br>'
        body_footer= 'Cordiali saluti<br><br>' + user_fullname + '<br><br>' + ag_fullstyle + """</span></div>"""
        
        body_msg=("""<span style="font-family:courier new,courier,monospace;">""" + sal + '<br>' + "con la presente siamo a richiederVi fornitura di tonn."+qt_ws +" di acqua poatbile per " +vessel_type + ' ' + vessel_name + " :" + '<br><br>' +
                       'Potete fatturare a:<br>' + int_fat + '<br><br> e inviare a:<br>' + agency_name + '<br><br>')
        body_html=(body_msg + body_footer )
        #print(x)
        
        self.db.table('email.message').newMessage(account_id=account_email,
                           to_address=email_to,
                           from_address=email_mittente,
                           subject=subject, body=body_html, 
                           cc_address=email_cc,
                           html=True)
        self.db.commit()
        
        nome_temp='ws'
        return nome_temp

    @public_method
    def email_arrival_sof(self, record,email_template_id=None,servizio=[],selPkeys_att=None, **kwargs):
        tbl_arrival = self.db.table('shipsteps.arrival')
        
        #verifichiamo che ci sia il record
        if not record:
            return
        #creiamo la variabile lista attcmt dove tramite il ciclo for andremo a sostituire la parola 'site' con '/home'
        attcmt=[]
        #verifichiamo che nei kwargs['allegati'] non abbiamo il valore nullo e trasformiamo la stringa pkeys allegati in una lista prelevandoli dai kwargs ricevuti tramite bottone
        if kwargs['allegati'] is not None:
            lista_all = list(kwargs['allegati'].split(","))
        else:
            lista_all = None
        
        #lettura degli attachment
        if lista_all is not None:
            len_allegati = len(lista_all) #verifichiamo la lunghezza della lista pkeys tabella allegati
            file_url=[]
            tbl_att =  self.db.table('shipsteps.arrival_atc') #definiamo la variabile della tabella allegati
            #ciclo for per la lettura dei dati sulla tabella allegati ritornando su ogni ciclo tramite la pkey dell'allegato la colonna $fileurl e alla fine
            #viene appesa alla variabile lista file_url
            for e in range(len_allegati):
                pkeys_att=lista_all[e]
                fileurl = tbl_att.readColumns(columns='$fileurl',
                      where='$id=:att_id',
                        att_id=pkeys_att)
                if fileurl is not None and fileurl !='':
                    file_url.append(fileurl)
        
            ln = len(file_url)
            for r in range(ln):
                fileurl = file_url[r]
                file_path = fileurl.replace('/home','site')
                fileSn = self.site.storageNode(file_path)
                attcmt.append(fileSn.internal_path) 

        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('shipsteps.staff')
        account_email,email_mittente = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('shipsteps.agency')
        account_emailpec = tbl_agency.readColumns(columns='$emailpec_account_id',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

        #verifichiamo e assegnamo alla variabile sof_id arrivatoci dal bottone di invio email
        if kwargs:
            sof_id=kwargs['sof_id']
            if sof_id is None:
                nome_temp='no_sof'
                return nome_temp
        else:
            return
        #inizializziamo le variabili per le email
        email_arr_to,email_arr_cc,email_arr_bcc='','',''
        email_a_to,email_a_cc,email_a_bcc=[],[],[]
        #definiamo le tabelle dove prelevare l'email
        tbl_email_sof=self.db.table('shipsteps.email_sof')
        tbl_email_arr=self.db.table('shipsteps.email_arr')
        #verifichiamo la lunghezza del servizio arrivatoci tramite il bottone di invio email e con i cicli for preleviamo i
        #dati email dalle relative tabelle- tramite l'uso delle liste con gli append aggiungiamo l'email 
        ln_serv=len(servizio)
        for e in range(ln_serv):
            serv=servizio[e]
            if serv=='arr':
                email_to = tbl_email_arr.query(columns="$email",
                                                    where='$arrival_id=:a_id and $email_type=:type', a_id=record,
                                                    type='to').fetch()
                for e in range(len(email_to)):
                    email_a_to.append(email_to[e][0])

                email_cc = tbl_email_arr.query(columns="$email",
                                                    where='$arrival_id=:a_id and $email_type=:type', a_id=record,
                                                    type='cc').fetch()  
                for e in range(len(email_cc)):
                    email_a_cc.append(email_cc[e][0])

                email_bcc = tbl_email_arr.query(columns="$email",
                                                    where='$arrival_id=:a_id and $email_type=:type', a_id=record,
                                                    type='ccn').fetch()
                for e in range(len(email_bcc)):
                    email_a_bcc.append(email_bcc[e][0])
                
            elif serv=='sof':
                email_to = tbl_email_sof.query(columns="$email",
                                                    where='$sof_id=:s_id and $email_type=:type', s_id=sof_id,
                                                    type='to').fetch()  
                for e in range(len(email_to)):
                    email_a_to.append(email_to[e][0])

                email_cc = tbl_email_sof.query(columns="$email",
                                                    where='$sof_id=:s_id and $email_type=:type', s_id=sof_id,
                                                    type='cc').fetch()
                for e in range(len(email_cc)):
                    email_a_cc.append(email_cc[e][0]) 

                email_bcc = tbl_email_sof.query(columns="$email",
                                                    where='$sof_id=:s_id and $email_type=:type', s_id=sof_id,
                                                    type='ccn').fetch()  
                for e in range(len(email_bcc)):
                    email_a_bcc.append(email_bcc[e][0])
        #estraiamo le stringhe email dalle liste
        email_arr_to=','.join([str(item) for item in email_a_to])
        email_arr_cc=','.join([str(item) for item in email_a_cc])                    
        email_arr_bcc=','.join([str(item) for item in email_a_bcc])
        #verifichiamo che non mancano email destinatari TO e CCN altrimenti ritorniamo con la variabile nome_temp che innesca il messaggio
        #verifichiamo se non presente l'email to allora inseriamo l'email del mittente
        if email_arr_to == email_arr_bcc == '':  
            nome_temp = 'no_email'
            return nome_temp
        elif email_arr_to =='':    
            email_arr_to=email_mittente 
        #creiamo il nuovo messaggio e con il db.commit lo salviamo nella tabella di uscita email pronto per l'invio                                        
        self.db.table('email.message').newMessageFromUserTemplate(
                                                          record_id=sof_id,
                                                          table='shipsteps.sof',
                                                          account_id = account_email,
                                                          to_address=email_arr_to,
                                                          cc_address=email_arr_cc,
                                                          bcc_address=email_arr_bcc,
                                                          attachments=attcmt,
                                                          template_code=email_template_id)
        self.db.commit()
        #ritorniamo con la variabile nome_temp per l'innesco del messaggio e il settaggio della checklist invio email a vero
        if email_template_id == 'email_updating_shiprec':
            nome_temp = 'ship_rec_upd'
        else:
            nome_temp = 'ship_rec'
        return nome_temp

    @public_method
    def print_template(self, record, resultAttr=None, nome_template=None, email_template_id=None,servizio=[],  nome_vs=None, format_page=None, **kwargs):
        # Crea stampa
        self.vessel_name = nome_vs
        tbl_arrival = self.db.table('shipsteps.arrival')
        builder = TableTemplateToHtml(table=tbl_arrival)
        #nome_template = nome_template #'shipsteps.arrival:check_list'

        nome_temp = nome_template.replace('shipsteps.arrival:','')
        if nome_template == 'shipsteps.arrival:mod61_arr' or nome_template == 'shipsteps.arrival:mod61_dep':
            nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp +'_' + nome_vs)
        else:
            nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)
        #nome_file_st = 'laboratorio_piazza_sta_{cl_id}.pdf'.format(
        #    cl_id=self.avatar.user_id)
        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)
        
       #tbl_template=self.db.table('adm.htmltemplate')
       #letterhead = tbl_template.readColumns(columns='$id',
       #          where='$name=:tp_name', tp_name='A3_orizz')
        # (pdfpath.internal_path)
        #print(x)
       #if kwargs:
       #    letterhead=kwargs['letterhead_id']
       #else:
       #    letterhead=''
        
        #Verifichiamo nel caso stampa sia del mod61_arr se ci sono i file da allegare in cartella altrimenti ritorniamo con il msg di errore
        if nome_temp == 'mod61_arr':
            nome_fal1arr = 'Fal1_arr_' + nome_vs
            nome_notarr = 'Nota_arrivo_' + nome_vs
            self.fal1_path = self.site.site_path+'/stampe_template/'+nome_fal1arr+'.pdf'
            self.notacp_path = self.site.site_path+'/stampe_template/'+nome_notarr+'.pdf'
            if not os.path.isfile(self.fal1_path):
                fal1_arrival = 'no'
            else:
                fal1_arrival = 'yes'    
            if not os.path.isfile(self.notacp_path):
                nota_arrivo = 'no'
            else:
                nota_arrivo = 'yes'
           
            if fal1_arrival == 'no' and nota_arrivo == 'no':
                nome_temp = 'fal1arr_notarr'  
                return nome_temp      
            elif fal1_arrival=='no':
                nome_temp = 'fal1_arr_no'
                return nome_temp
            elif nota_arrivo == 'no':
                nome_temp='nota_arr_no'
                return nome_temp
        
        if nome_temp == 'mod61_dep':
            sailed= self.db.table('shipsteps.arrival').readColumns(columns="$ets", where='$id=:a_id',a_id=record)
            if sailed is None:
                nome_temp = 'no_sailed'
                return nome_temp
            nome_fal1dep = 'Fal1_dep_' + nome_vs
            nome_notdep = 'Dich_integrativa_partenza_' + nome_vs
            self.fal1_path = self.site.site_path+'/stampe_template/'+nome_fal1dep+'.pdf'
            self.notacp_path = self.site.site_path+'/stampe_template/'+nome_notdep+'.pdf'
            if not os.path.isfile(self.fal1_path):
                fal1_departure = 'no'
            else:
                fal1_departure = 'yes'    
            if not os.path.isfile(self.notacp_path):
                nota_partenza = 'no'
            else:
                nota_partenza = 'yes'
           
            if fal1_departure == 'no' and nota_partenza == 'no':
                nome_temp = 'fal1dep_notapart'  
                return nome_temp      
            elif fal1_departure=='no':
                nome_temp = 'fal1_dep_no'
                return nome_temp
            elif nota_partenza == 'no':
                nome_temp='nota_part_no'
                return nome_temp

        builder(record=record, template=template)#,letterhead_id=letterhead)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)
        
        self.setInClientData(path='gnr.clientprint',
                             value=result.url(timestamp=datetime.now()), fired=True)
       #inseriamo nella tabella di attachment il mod61_arr 
       #if nome_temp == 'mod61_arr':
       #    tbl_arrival_atc = self.db.table('shipsteps.arrival_atc')
       #    if not tbl_arrival_atc.checkDuplicate(maintable_id=record,description=nome_file):
       #        
       #        tbl_arrival_atc.addAttachment(maintable_id=record,
       #                                     origin_filepath=pdfpath,
       #                                     description=nome_file,
       #                                     copyFile=True)

        #inviamo l'email se si tratta di mod61_arr e rispetta le condizioni dei file da allegare
        if nome_temp == 'mod61_arr':
            if  fal1_arrival == 'yes' and nota_arrivo == 'yes':
                self.email_services(record,email_template_id,servizio, nome_temp, **kwargs)
                return nome_temp
        #inviamo l'email se si tratta di mod61_dep e rispetta le condizioni dei file da allegare
        if nome_temp == 'mod61_dep':
            if  fal1_departure == 'yes' and nota_partenza == 'yes':
                self.email_services(record,email_template_id,servizio, nome_temp, **kwargs)
                return nome_temp
        #inviamo l'email se si tratta di immigration form e rispetta le condizioni dei file da allegare
        if kwargs:
            for chiave in kwargs.keys():
                if chiave == 'only_print':
                    if kwargs['only_print'] == 'yes':
                        return
        if nome_temp == 'form_immigration' :
            self.email_services(record,email_template_id,servizio, nome_temp, **kwargs)
            return nome_temp        
        return nome_temp

    @public_method
    def print_template_garbage(self, record, resultAttr=None,selId=None, nome_template=None, email_template_id=None,servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        selPkeys_att=kwargs['selPkeys_att']
        if selId is None:
            nome_temp = 'yes'
            return nome_temp

        tbl_garbage = self.db.table('shipsteps.garbage')
        builder = TableTemplateToHtml(table=tbl_garbage)

        nome_temp = nome_template.replace('shipsteps.garbage:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        builder(record=selId, template=template)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)
        self.email_services(record,email_template_id,servizio, **kwargs)
        #se ritorna il valore di nome_temp dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di nome_temp alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
        nome_temp='val_garbage'
        return nome_temp

    @public_method
    def print_template_derogagb(self, record, resultAttr=None,selId=None,moored=None, nome_template=None, email_template_id=None,servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        #facciamo arrivare alla variabile moored la datetime dell'ormeggio e se non presente torna indietro il messaggio no_moored per far scattare il dataController
        if moored is None or moored == '':
            nome_temp = 'no_moored'
            return nome_temp

        tbl_arrival = self.db.table('shipsteps.arrival')
        builder = TableTemplateToHtml(table=tbl_arrival)

        nome_temp = nome_template.replace('shipsteps.arrival:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        builder(record=record, template=template)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)
        self.email_services(record,email_template_id,servizio, **kwargs)
        #se ritorna il valore di nome_temp dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di self.ms_special alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
        nome_temp='val_deroga_gb'
        return nome_temp    
    
    @public_method
    def apridoc(self,record,nome_form=None, **kwargs):
        workport=record['workport']
        eta=record['eta'].strftime("%d/%m/%Y")
        etb=record['etb'].strftime("%d/%m/%Y")
        lastport=record['lastport']
        nextport=record['nextport']
        vesselname=record['vesselname']
        flag=record['flag']
        imo=record['imo']
        gt=record['tsl']
        master_name=record['master_name']
        crew_n=str(record['n_crew'])
        pax_n=str(record['n_passengers'])
        vessel_details_id=record['vessel_details_id']
        workdate = self.db.workdate.strftime("%d/%m/%Y")
        if nome_form=='DichSanimare':
            #cerchiamo nella tabella certificati nave la sanitation
            tbl_shipsdoc = self.db.table('shipsteps.ship_doc')
            sanitation = tbl_shipsdoc.query(columns="$issued,to_char($date_cert,:df)", where='$cert=:cert and $vessel_details=:vess_det', 
                                                            cert='06_sanitation',vess_det=vessel_details_id, df='DD/MM/YYYY').fetch() 
            if sanitation == []:
                nome_temp ='no_sanitation'
                return nome_temp
            san_place_id = sanitation[0][0]
            san_date = sanitation[0][1]
            #san_place_id,san_date=tbl_shipsdoc.readColumns(columns="$issued,to_char($date_cert,:df)", where='$cert=:cert and $vessel_details=:vess_det', 
            #                                                cert='06_sanitation',vess_det=vessel_details_id, df='DD/MM/YYYY')
            #tramite l'id del luogo di rilascio del certificato andiamo a cercare nella tabella degli unlocode il place
            tbl_place = self.db.table('unlocode.place')
            san_place=tbl_place.readColumns(columns="$descrizione || ' - ' || @nazione_code.nome", where='$id=:place_id', place_id=san_place_id)
        
            nome_file = 'DichSanimare.docx'
            file_sn_out = self.site.storageNode('home:form_standard', 'DichSanimare_filled.docx')
           
            variables = {
            "${porto}": workport,
            "${date_arr}": eta,
            "${etb}": etb,
            "${nome_imb}": vesselname,
            "${imo}": imo,
            "${last_port}": lastport,
            "${next_port}": nextport,
            "${flag}": flag,
            "${master_name}": master_name,
            "${gt}": gt,
            "${sanitation_place}": san_place,
            "${date_sanitation}": str(san_date),
            "${crew_n}": crew_n,
            "${pax_n}": pax_n,
            "${current_date}": workdate,
            "${medico}": "/////",
            }
        if nome_form == 'InterferenzeFiore':
            nome_file = 'InterferenzeFiore.docx'
            file_sn_out = self.site.storageNode('home:form_standard', 'InterferenzeFiore_filled.docx')    
            variables = {
            "${etb}": etb,
            "${nome_imb}": vesselname,
            }
        file_sn = self.site.storageNode('home:form_standard', nome_file)
        template_file_path = file_sn.internal_path
        #template_file_path = '/home/tommaso/Documenti/Linux/Python/ModificaDocx/test.docx'
        
        output_file_path = file_sn_out.internal_path
        #output_file_path = '/home/tommaso/Documenti/Linux/Python/ModificaDocx/result.docx'
        
        

        template_document = Document(template_file_path)

        for variable_key, variable_value in variables.items():
            for paragraph in template_document.paragraphs:
                self.replace_text_in_paragraph(paragraph, variable_key, variable_value)

            for table in template_document.tables:
                for col in table.columns:
                    for cell in col.cells:
                        for paragraph in cell.paragraphs:
                            self.replace_text_in_paragraph(paragraph, variable_key, variable_value)
        
        template_document.save(output_file_path)
        #apriamo direttamente il file salvato con il programma standard di sistema
        filename=output_file_path
        subprocess.call(('xdg-open', filename))

    def replace_text_in_paragraph(self,paragraph, key, value):
        if key in paragraph.text:
            inline = paragraph.runs
            for item in inline:
                if key in item.text:
                    item.text = item.text.replace(key, value)
        


    
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
   
    
    