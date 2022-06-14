#!/usr/bin/python3
# -*- coding: utf-8 -*-

from turtle import left
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
from gnr.core.gnrlang import GnrException

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id', width='7em')
        r.fieldcell('reference_num', width='7em')
        r.fieldcell('visit_id',width='8em')
        r.fieldcell('nsis_prot',width='8em')
        r.fieldcell('date')
        r.fieldcell('vessel_details_id', width='15em')
        r.fieldcell('eta', width='5em')
        r.fieldcell('etb', width='5em')
        r.fieldcell('et_start', width='5em')
        r.fieldcell('etc', width='5em')
        r.fieldcell('ets', width='5em')
        r.fieldcell('draft_aft_arr', width='5em')
        r.fieldcell('draft_fw_arr', width='5em')
        r.fieldcell('draft_aft_dep', width='5em')
        r.fieldcell('draft_fw_dep', width='5em')
        r.fieldcell('n_tug',width='4em')
        r.fieldcell('mandatory')
        r.fieldcell('dock_id', width='5em')
        r.fieldcell('info_moor')
        r.fieldcell('master_name')
        r.fieldcell('n_crew', width='5em')
        r.fieldcell('n_passengers', width='5em')
        r.fieldcell('last_port', width='7em')
        r.fieldcell('departure_lp', width='5em')
        r.fieldcell('next_port', width='7em')
        r.fieldcell('eta_np', width='5em')
        r.fieldcell('cargo_dest')
        r.fieldcell('invoice_det_id', width='40em')
        r.fieldcell('@gpg_arr.n_gpg', name= 'GPG n.')
        r.fieldcell('@gpg_arr.date_start', name= 'GPG start', width='5em')
        r.fieldcell('@gpg_arr.date_end', name= 'GPG end', width='5em')
       #r.fieldcell('@cargo_lu_arr.description', name= 'cargo_descr', width='5em')
        #r.fieldcell('carico', name='Descrizione Carico',width='30em')
        #r.fieldcell('cargo', width='50em')
        #r.fieldcell('@cargo_lu_arr.cargo_on_board', width='50em')
        r.fieldcell('cargo_lu_en', width='50em')
        r.fieldcell('@cargo_lu_arr.tot_cargo', width='10em')
        r.fieldcell('ship_rec', width='30em')

    def th_order(self):
        return 'reference_num:d' 

    def th_query(self):
        return dict(column='reference_num', op='contains', val='', runOnStart=True)



class Form(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        #pane = form.record
        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        tc = form.center.tabContainer()
        #bc1 = form.center.borderContainer()
        #tc = bc1.tabContainer(margin='2px', region='center', height='auto', splitter=True)

        bc = tc.borderContainer(title='!![en]Arrival')
        bc_att = tc.borderContainer(title='!![en]Attachments')
        tc_task = tc.tabContainer(title='!![en]Task List',region='center',selectedPage='^.pippo')
        bc_tasklist = tc_task.borderContainer(title='!![en]Task List', region='center')
       # tc_task = tc_task.tabContainer(title='!![en]Shore Pass')
        #tc_shorepass = tc_task.tabContainer(title='!![en]Shore Pass', region='center')
        #tc_prova = tc_task.tabContainer(title='!![en]prova')
        tc_undertask = bc_tasklist.tabContainer(margin='2px', region='center', height='auto')
        tc_sof = tc.borderContainer(title='!![en]SOF')
        tc_app = tc.tabContainer(title='!![en]Applications')
        #tc_parapon = bc_task3.tabContainer(title='pippo')
        self.allegatiArrivo(bc_att.contentPane(title='!![en]Attachments', height='100%'))
       # tc2 = bc2.tabContainer(margin='2px', region='center', height='auto', splitter=True)
       # bc_top = bc.borderContainer(region='center',height='300px', splitter=True)
       # pane_center=bc_top.contentPane(region='center',datapath='.record', width='1200px', splitter=True)
        #pane_center=bc_top.contentPane(region='center',datapath='.record', width='1100px', splitter=True)
       # pane_right=bc_top.contentPane(region='right',datapath='.@gpg_arr', width='320px', splitter=True)
        self.datiArrivo(bc.borderContainer(region='top',height='300px', splitter=True, background = 'lavenderblush'))
       
        self.taskList(bc_tasklist.borderContainer(region='top',height='50%', background = 'lavenderblush', splitter=True))
        self.shorepass(tc_task.contentPane(title='!![en]Shore pass'))
        self.services(tc_task.contentPane(title='!![en]Vessel Services',pageName='services'))
        self.sof(tc_sof.contentPane(title='!![en]Sof',height='100%'))
        
        #self.allegatiArrivo(tc_task.contentPane(title='Attachments', region='center', height='100%', splitter=True))
        
        self.garbage(tc_undertask.contentPane(title='!![en]Garbage'))
        self.rinfusa(tc_app.contentPane(title='!![en]Bulk Application'))
        self.bunker(tc_app.contentPane(title='!![en]Bunker Application'))
        
        #self.datiArrivo(pane_center)
        #self.datiArrivo(pane_center)
        #self.gpg(bc.borderContainer(region='center',datapath='.@gpg_arr',height='300px', splitter=True, background = 'lavenderblush'))

        tc = bc.tabContainer(margin='2px', region='center', height='auto', splitter=True)
        tc_car = tc.tabContainer(title='!![en]Cargo',margin='2px', region='center', height='auto', splitter=True)
        #tc_sof = tc.tabContainer(title='!![en]SOF',margin='2px', region='center', height='450px', splitter=True)
        #tc_r = bc_top.tabContainer(margin='2px', region='right', width='25%')#, width='25%', splitter=True)
        #self.gpg(tc_r.contentPane(title='!![en]GPG'))

        self.datiCaricoBordo(tc_car.contentPane(title='!![en]Cargo onboard',datapath='.record'))
        self.datiCarico(tc_car.contentPane(title='!![en]Cargo loading / unloading'))
        self.datiCaricoTransit(tc_car.contentPane(title='!![en]Transit cargo',datapath='.record'))
        self.car_ric(tc.contentPane(title='!![en]Shippers / Receivers'))
        self.charterers(tc.contentPane(title='!![en]Charterers'))
       # self.sof(tc.contentPane(title='!![en]Sof'))
        self.arrival_details(tc.borderContainer(title='!![en]Arrival/Departure details', region='top', background = 'lavenderblush'))
        self.emailArrival(tc.contentPane(title='!![en]Email Arrival'))
        #self.taskList(tc.borderContainer(title='!![en]Task list', region='top', background = 'lavenderblush'))

        #self.sof_cargo(tc_sof.contentPane(title='!![en]Sof_Cargo', datapath='.@sof_arr'))
    def services(self,pane):
        #pass
        #pane.inlineTableHandler(relation='@garbage_arr',viewResource='ViewFromGarbage')
        pane.inlineTableHandler(relation='@vess_services',viewResource='ViewFromVesselServices')

    def datiArrivo(self,bc):
        center = bc.roundedGroup(title='!![en]Vessel arrival', region='center',datapath='.record',width='210px', height = '100%').div(margin='10px',margin_left='2px')
        center1 = bc.roundedGroup(title='!![en]Arrival details',region='center',datapath='.record',width='960px', height = '100%', margin_left='210px').div(margin='10px',margin_left='2px')
        center2 = bc.roundedGroup(title='!![en]Special security guards',table='shipsteps.gpg',region='center',datapath='.record.@gpg_arr',width='240px', height = '150px', margin_left='1170px').div(margin='10px',margin_left='2px')
        center3 = bc.roundedGroup(title='!![en]EXTRA',region='center',datapath='.record',width='240px', height = '50%', margin_left='1170px', margin_top='150px').div(margin='10px',margin_left='2px')
        #center3 = bc.roundedGroup(title='!![en]Times',table='shipsteps.arrival_time',region='center',datapath='.record.@time_arr',width='245px', height = '350px', margin_left='1385px').div(margin='10px',margin_left='2px')

        fb = center.formbuilder(cols=1, border_spacing='4px',lblpos='T')
        fb.field('agency_id', readOnly=True )
        fb.field('reference_num', readOnly=True)
        fb.field('date')
        fb.field('vessel_details_id',validate_notnull=True )
        fb.field('pfda_id' , hasDownArrow=True,  auxColumns='$data,@imbarcazione_id.nome')
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
        fb.field('last_port',auxColumns='@nazione_code.nome' )
        fb.field('departure_lp' , width='10em')
        fb.field('next_port',auxColumns='@nazione_code.nome' )
        fb.field('eta_np' , width='10em')
        fb.br()
        fb.field('mandatory', colspan=3 , width='47em')
        fb.field('cargo_dest', colspan=2, width='29em' )
        fb.br()
        fb.field('invoice_det_id',colspan=5 ,width='78em', hasDownArrow=True)

        fb = center2.formbuilder(cols=1, border_spacing='4px', fld_width='10em')
        #fb.field('arrival_id')
        fb.field('date_start')
        fb.field('date_end')
        fb.field('n_gpg')

        fb = center3.formbuilder(cols=1, border_spacing='4px', fld_width='10em')
        fb.field('nsis_prot')
        fb.field('n_tug')

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

    def datiCaricoBordo(self,frame):
        frame.simpleTextArea(title='!![en]Cargo on board',value='^.cargo_onboard',editor=True,validate_notnull=True)

    def datiCarico(self,pane):
        pane.inlineTableHandler(relation='@cargo_lu_arr',viewResource='ViewFromCargoLU')

    def datiCaricoTransit(self,frame):
        frame.simpleTextArea(title='!![en]Transit cargo',value='^.transit_cargo',editor=True)

    def car_ric(self,pane):
         pane.stackTableHandler(table='shipsteps.ship_rec', formResource='Form',view_store_onStart=True)

        #pane.inlineTableHandler(table='shipsteps.ship_rec',viewResource='ViewFromShipRec',view_store_onStart=True,export=True)

    def charterers(self,pane):
        pane.inlineTableHandler(table='shipsteps.charterers',viewResource='ViewFromCharterers',view_store_onStart=True,export=True)

    def sof(self,pane):
        pane.stackTableHandler(relation='@sof_arr', formResource='FormSof')

    def arrival_details(self, bc):
        rg_times = bc.roundedGroup(title='!![en]Arrival/Departure times',table='shipsteps.arrival_time',region='left',datapath='.record.@time_arr',width='350px', height = 'auto').div(margin='10px',margin_left='2px')
        rg_details = bc.roundedGroup(title='!![en]Arrival/Departure details',table='shipsteps.arrival_det', region='center',datapath='.record.@arr_details',width='auto', height = 'auto').div(margin='10px',margin_left='2px')

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
        fb = div_draft.formbuilder(cols=3, border_spacing='4px',fld_width='10em')
        #fb = rg_details.formbuilder(cols=3, border_spacing='4px',fld_width='10em')

        #fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=3, border_spacing='4px',fld_width='10em',table='shipsteps.arrival_det',datapath='.record.@arr_details')
        #fb.div('!![en]<strong>DRAFT</strong>')
        fb.br()
        fb.field('draft_aft_arr',placeholder='e.g. 4,5')
        fb.field('draft_fw_arr',placeholder='e.g. 4,5')
        fb.br()
        fb.field('draft_aft_dep',placeholder='e.g. 4,5')
        fb.field('draft_fw_dep',placeholder='e.g. 4,5')
        fb.br()
        div_rem=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>REMAINS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_rem.formbuilder(cols=3, border_spacing='4px',fld_width='10em')

        #fb.div('!![en]<strong>REMAINS</strong>')
        fb.br()
        fb.field('ifo_arr',placeholder='e.g. mt.50')
        fb.field('do_arr',placeholder='e.g. mt.50')
        fb.field('lo_arr',placeholder='e.g. kgs.50')
        fb.field('ifo_dep',placeholder='e.g. mt.50')
        fb.field('do_dep',placeholder='e.g. mt.50')
        fb.field('lo_dep',placeholder='e.g. kgs.50')
        fb.br()
        div_fw=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>FRESH WATER</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_fw.formbuilder(cols=3, border_spacing='4px',fld_width='10em')
        #fb.div('!![en]<strong>FRESH WATER</strong>')
        fb.br()
        fb.field('fw_arr',placeholder='e.g. mt.50')
        fb.field('fw_dep',placeholder='e.g. mt.50')
        fb.br()
        div_tug=rg_details.div('&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<strong>USED TUGS</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb = div_tug.formbuilder(cols=3, border_spacing='4px',fld_width='10em')
        #fb.div('!![en]<strong>USED TUGS</strong>')
        fb.br()
        fb.field('tug_in',placeholder='e.g. 1')
        fb.field('tug_out',placeholder='e.g. 1')

    def emailArrival(self,pane):
        pane.inlineTableHandler(title='!![en]Email arrival',relation='@arrival_email',viewResource='ViewFromEmailArrival')
   #def sof_cargo(self,pane):
   #    pane.inlineTableHandler(table='shipsteps.sof_cargo', viewResource='ViewFromSof_Cargo')
    

    def taskList(self, bc_tasklist):
        rg_prearrival = bc_tasklist.roundedGroup(title='!![en]Pre arrival',table='shipsteps.tasklist',region='left',datapath='.record.@arr_tasklist',width='550px', height = 'auto').div(margin='10px',margin_left='2px')
        rg_arrival = bc_tasklist.roundedGroup(title='!![en]Arrival/Departure',table='shipsteps.tasklist',region='center',datapath='.record.@arr_tasklist',width='500px', height = 'auto').div(margin='10px',margin_left='2px')
        #rg_departure = bc_tasklist.roundedGroup(title='!![en]Departure',table='shipsteps.tasklist',region='center',datapath='.record.@arr_tasklist',width='340px', height = 'auto',margin_left='350px').div(margin='10px',margin_left='2px')
        #rg_prearrival_cp = bc_task.roundedGroup(title='!![en]Pre arrival CP',table='shipsteps.tasklist',region='left',datapath='.record.@arr_tasklist',width='670px', height = 'auto',margin_top='290px').div(margin='10px',margin_left='2px')
        #rg_details = bc.roundedGroup(title='!![en]Arrival details',table='shipsteps.arrival_det', region='center',datapath='.record.@arr_details',width='auto', height = 'auto').div(margin='10px',margin_left='2px')
       #tbl_staff =  self.db.table('shipsteps.staff')
       #account_email = tbl_staff.readColumns(columns='$email_account_id',
       #          where='$agency_id=:ag_id',
       #            ag_id=self.db.currentEnv.get('current_agency_id'))
       #tbl_agency =  self.db.table('shipsteps.agency')
       #account_emailpec = tbl_agency.readColumns(columns='$emailpec_account_id',
       #          where='$id=:ag_id',
       #            ag_id=self.db.currentEnv.get('current_agency_id'))
        #,fld_width='10em')
        #fb.field('arrival_id')

        #definizione primo rettangolo di stampa all'interno del roundedGroup Pre Arrival
        div1=rg_prearrival.div(width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb1=div1.formbuilder(colspan=3,cols=9, border_spacing='1px')

        btn_cl = fb1.Button('!![en]Print Check list',width='122px')
        btn_cl.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id',
                            nome_template = 'shipsteps.arrival:check_list', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',format_page='A4')
        fb1.dataController("if(msg=='check_list') SET .checklist=true", msg='^nome_temp')
        fb1.field('checklist', lbl='', margin_top='5px')
        fb1.semaphore('^.checklist', margin_top='5px')
        btn_fs = fb1.Button('!![en]Print Frontespicie', width='146px')
        btn_fs.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:front_nave',format_page='A4')
        fb1.dataController("if(msg=='front_nave') SET .frontespizio=true", msg='^nome_temp')
        fb1.field('frontespizio', lbl='', margin_top='5px')
        fb1.semaphore('^.frontespizio', margin_top='5px')

        btn_cn = fb1.Button('!![en]Print Vessel folder', width='122px')
       #btn_cn.dataRpc(None, self.print_template,record='=#FORM.record.id',_ask=dict(title='!![en]Choose lettehead to use with this form',
       #                                        fields=[dict(name='letterhead_id', lbl='!![en]Letterhead', tag='dbSelect',columns='$id',
       #                                        hasDownArrow=True, auxColumns='$name', table='adm.htmltemplate')]), nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
       #                    nome_template = 'shipsteps.arrival:cartella_doc')
        btn_cn.dataRpc('nome_temp', self.print_template, record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:cartella_doc',format_page='A3')
        fb1.dataController("if(msg=='cartella_doc') SET .cartella_nave=true", msg='^nome_temp')
        fb1.field('cartella_nave', lbl='', margin_top='5px')
        fb1.semaphore('^.cartella_nave', margin_top='5px')

        btn_ts = fb1.Button('!![en]Print Servicies table')
        btn_ts.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:tab_servizi',format_page='A3')
        fb1.dataController("if(msg=='tab_servizi') SET .tab_servizi=true", msg='^nome_temp')
        fb1.field('tab_servizi', lbl='', margin_top='5px')
        fb1.semaphore('^.tab_servizi', margin_top='5px')

        btn_fc = fb1.Button('!![en]Print Cargo frontespiece')
        btn_fc.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:front_carico',format_page='A4')
        fb1.dataController("if(msg=='front_carico') SET .front_carico=true", msg='^nome_temp')
        fb1.field('front_carico', lbl='', margin_top='5px')
        fb1.semaphore('^.front_carico', margin_top='5px')

        btn_mn = fb1.Button('!![en]Print Vessel module',action="SET .modulo_nave=true")
        btn_mn.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:mod_nave',format_page='A4')
        fb1.dataController("if(msg=='mod_nave') SET .checklist=true", msg='^nome_temp')
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
        btn_sr.dataRpc('msg_special', self.email_arrival_sof,
                   record='=#FORM.record.id', servizio=['arr','sof'], email_template_id='email_arr_shiprec',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the SOF and Attachments',fields=[dict(name='sof_id', lbl='!![en]sof', tag='dbSelect',columns='$id',
                             hasDownArrow=True, auxColumns='$sof_n,$ship_rec', table='shipsteps.sof',condition="$arrival_id =:cod",
                                                condition_cod='=#FORM.record.id',width='25em',validate_notnull=True),dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.field('email_ship_rec',lbl='', margin_top='5px')
        fb.semaphore('^.email_ship_rec', margin_top='5px')
        #datacontroller verifica il valore della variabile msg_special di ritorno dalla funzione per invio email
        #e setta il valore della campo checkbox a true e lancia il messaggio 'Messaggio Creato'
        fb.dataController("if(msgspec=='ship_rec') {SET .email_ship_rec=true ; alert('Message created')} if(msgspec=='no_email') alert('You must insert destination email as TO or BCC'); if(msgspec=='no_sof') alert('You must select the SOF or you must create new one');", msgspec='^msg_special')
        
        btn_dog = fb.Button('!![en]Customs',width='80px')
        btn_dog.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['dogana','gdf','gdf roan'], email_template_id='email_dogana',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                    _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        #datacontroller verifica il valore della variabile msg_special di ritorno dalla funzione per invio email
        #e setta il valore della campo checkbox a true e lancia il messaggio 'Messaggio Creato'
        fb.dataController("if(msgspec=='val_dog') {SET .email_dogana=true ; alert('Message created')}", msgspec='^msg_special')
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
        btn_fr.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['immigration'], email_template_id='email_frontiera',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_imm') {SET .email_frontiera=true; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_frontiera',lbl='', margin_top='5px')
        fb.semaphore('^.email_frontiera', margin_top='5px')

        btn_usma = fb.Button('!![en]Sanimare',width='115px')
        btn_usma.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['sanimare'], email_template_id='email_sanimare',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_usma') {SET .email_usma=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_usma',lbl='', margin_top='5px')
        fb.semaphore('^.email_usma', margin_top='5px')

        btn_pilot = fb.Button('!![en]Pilot/Moor',width='80px')
        btn_pilot.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['pilot','mooringmen'], email_template_id='email_pilot_moor',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_pil_moor') {SET .email_pilot_moor=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_pilot_moor',lbl='', margin_top='5px')
        fb.semaphore('^.email_pilot_moor', margin_top='5px')

        btn_tug = fb.Button('!![en]Tug', width='98px')
        btn_tug.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['tug'], email_template_id='email_tug',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_tug') {SET .email_tug=true ; alert('Message created')}", msgspec='^msg_special')
        #fb.dataController("alert(msg)", _if='msg',msg='^msg_special')
        fb.field('email_tug',lbl='', margin_top='5px')
        fb.semaphore('^.email_tug', margin_top='5px')

        btn_garb = fb.Button('!![en]Garbage', width='115px')
        btn_garb.dataRpc('msg_special', self.print_template_garbage,record='=#FORM.record.id',servizio=['garbage'], email_template_id='garbage_email',
                            nome_template = 'shipsteps.garbage:garbage_request',format_page='A4',selId='=#FORM.shipsteps_garbage.view.grid.selectedId',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        #fb.dataController("alert(msg)", _if='msg',msg='^msg_select')
        fb.dataController("if(msgspec=='val_garbage') {SET .email_garbage=true ; alert('Message created');} if(msgspec=='yes') alert('You must select the record as row in the garbage form'); "
                            , msgspec='^msg_special')
        fb.field('email_garbage',lbl='', margin_top='5px')
        fb.semaphore('^.email_garbage', margin_top='5px')
        
        btn_pfso = fb.Button('!![en]PFSO', width='80px')
        btn_pfso.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['pfso'], email_template_id='email_pfso',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_pfso') {SET .email_pfso=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_pfso',lbl='', margin_top='5px')
        fb.semaphore('^.email_pfso', margin_top='5px')

        btn_chem = fb.Button('!![en]Chemist', width='98px')
        btn_chem.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['chemist'], email_template_id='email_chemist',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                    _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_chemist') {SET .email_chemist=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_chemist',lbl='', margin_top='5px')
        fb.semaphore('^.email_chemist', margin_top='5px')

        btn_gpg = fb.Button('!![en]GPG', width='115px')
        btn_gpg.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['gpg'], email_template_id='email_gpg',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_gpg') {SET .email_gpg=true ; alert('Message created')}", msgspec='^msg_special')
        fb.field('email_gpg',lbl='', margin_top='5px')
        fb.semaphore('^.email_gpg', margin_top='5px')

        btn_ens = fb.Button('!![en]ENS', width='80px')
        btn_ens.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['ens'], email_template_id='email_ens',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_ens') {SET .email_ens=true ; alert('Message created')}", msgspec='^msg_special')
       # fb.dataController('SET .email_ens=True',__if='msg',msg='^msg_special')
        fb.field('email_ens',lbl='', margin_top='5px')
        fb.semaphore('^.email_ens', margin_top='5px')

        btn_ens = fb.Button('!![en]Garbage ADSP')
        btn_ens.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['adsp'], email_template_id='not_rifiuti',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',validate_notnull=True,
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_adsp') {SET .email_garbage_adsp=true ; alert('Message created')}", msgspec='^msg_special')
       # fb.dataController('SET .email_ens=True',__if='msg',msg='^msg_special')
        fb.field('email_garbage_adsp',lbl='', margin_top='5px')
        fb.semaphore('^.email_garbage_adsp', margin_top='5px')


       #btn_af = fb.Button('!![en]Email Antifire', width='101px')
       #fb.field('email_antifire',lbl='', margin_top='5px')
       #fb.semaphore('^.email_antifire', margin_top='5px')

        btn_update = fb.Button('!![en]services<br>updating', width='115px')
        btn_update.dataRpc('msg_special', self.email_serv_upd,
                   record='=#FORM.record',email_template_id='email_arr_shiprec',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the services to update and Attachments',fields=[dict(name='services', lbl='!![en]Services', tag='checkboxtext',
                             table='shipsteps.services_for_email', columns='$description_serv',#values='dogana,gdf,gdf roan,pilot,mooringmen,tug,immigration,sanimare,pfso,garbage,chemist,gpg',
                             validate_notnull=True,cols=4,popup=True,colspan=2),dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb.dataController("if(msgspec=='val_upd') {alert('Message created')}", msgspec='^msg_special')
        
        fb.div()
        fb.div()
     
        btn_upd_shiprec = fb.Button('!![en]Ship/Rec.<br>updating',width='80px')
        btn_upd_shiprec.dataRpc('msg_special', self.email_arrival_sof,
                   record='=#FORM.record.id', servizio=['arr','sof'], email_template_id='email_updating_shiprec',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                   _ask=dict(title='!![en]Select the SOF and Attachments',fields=[dict(name='sof_id', lbl='!![en]sof', tag='dbSelect',columns='$id',
                             hasDownArrow=True, auxColumns='$sof_n,$ship_rec', table='shipsteps.sof',condition="$arrival_id =:cod",
                                                condition_cod='=#FORM.record.id',width='25em',validate_notnull=True),dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        #datacontroller verifica il valore della variabile msg_special di ritorno dalla funzione per invio email
        #e setta il valore della campo checkbox a true e lancia il messaggio 'Messaggio Creato'
        fb.dataController("if(msgspec=='ship_rec_upd') {alert('Message created')} if(msgspec=='no_email') alert('You must insert destination email as TO or BCC'); if(msgspec=='no_sof') alert('You must select the SOF or you must create new one');", msgspec='^msg_special')
        
        div3=rg_prearrival.div('<center><strong>Harbour Master - Docs before vessel arrival</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb2 = div3.formbuilder(colspan=3,cols=9, border_spacing='2px')
        btn_integr = fb2.Button('!![en]Email Alimentary integration')
        btn_integr.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_integrazione_alim',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb2.dataController("if(msgspec=='val_integr') {SET .email_integr=true ; alert('Message created')}", msgspec='^msg_special')
       # fb.dataController('SET .email_ens=True',__if='msg',msg='^msg_special')
        fb2.field('email_integr', lbl='', margin_top='6px')
        fb2.semaphore('^.email_integr', margin_top='6px')

        btn_garb_cp = fb2.Button('!![en]Email Garbage form')
        btn_garb_cp.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_garbage_cp',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        fb2.dataController("if(msgspec=='val_garb_cp') {SET .email_garbage_cp=true ; alert('Message created')}", msgspec='^msg_special')
       # fb.dataController('SET .email_ens=True',__if='msg',msg='^msg_special')
        fb2.field('email_garbage_cp', lbl='', margin_top='6px')
        fb2.semaphore('^.email_garbage_cp', margin_top='6px')
        #definizione terzo rettangolo dentro rounded Group Pre Arrival CP
       #div_cp=rg_prearrival_cp.div(width='96%',height='60%',margin='auto',
       #                padding='5px',
       #                border='1px solid silver',
       #                margin_top='2px',margin_left='10px')
       #fb_cp=div_cp.formbuilder(colspan=3,cols=9, border_spacing='4px')
       #
       #btn_integr = fb_cp.Button('Email')
       #btn_integr.dataRpc('msg_special', self.email_services,
       #          record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_integrazione_alim')
       #fb_cp.dataController("if(msgspec=='val_integr') {SET .email_integr=true ; alert('Message created')}", msgspec='^msg_special')
      
       #fb_cp.field('email_integr', lbl='!![en]Alimentary integration')
       #fb_cp.semaphore('^.email_integr')
        fb.dataController("if(msgspec=='val_bulk') {alert('Message created')}", msgspec='^msg_special')
        
        div_arr=rg_arrival.div('<center><strong>ARRIVAL</strong>',width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px')
        fb_arr=div_arr.formbuilder(colspan=2,cols=4, border_spacing='1px')
        btn_chim_cp = fb_arr.Button('!![en]Email Cert. Chimico CP')
        btn_chim_cp.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_chimico_cp',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
                  _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',validate_notnull=True,
                             cols=4,popup=True,colspan=2)]))
        btn_chim_cp = fb_arr.Button('!![en]Email Waste derogation CP')
        btn_chim_cp.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_deroga_cp',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',
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
        
        
       

       

    def allegatiArrivo(self,pane):
        pane.attachmentGrid(viewResource='ViewFromArrivalAtc')

    def shorepass(self, pane):
        pane.stackTableHandler(relation='@shorepass_arr',formResource='Form')

    def garbage(self, pane):
        pane.inlineTableHandler(relation='@garbage_arr',viewResource='ViewFromGarbage')

    def rinfusa(self, pane):
        pane.stackTableHandler(relation='@rinfusa_arr',formResource='FormFromRinfusa')
    
    def bunker(self, pane):   
        pane.stackTableHandler(relation='@bunker_arr',formResource='FormFromBunker')

    @public_method
    def email_services(self, record,email_template_id=None,servizio=[],selPkeys_att=None, **kwargs):
        
        #creiamo la variabile lista attcmt dove tramite il ciclo for andremo a sostituire la parola 'site' con '/home'
        attcmt=[]
        #trasformiamo la stringa pkeys allegati in una lista prelevandoli dai kwargs ricevuti tramite bottone
        #ma verifichiamo se nei kwargs gli allegati ci sono per non ritrovarci la variabile lista_all senza assegnazione
        if kwargs['allegati'] is not None:
            lista_all=list(kwargs['allegati'].split(","))
        else:
            lista_all=None
        #lista_all=list(kwargs['allegati'].split(","))
        
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
                msg_special = 'val_dog'
            elif email_template_id == 'email_frontiera':
                msg_special = 'val_imm'
            elif email_template_id == 'email_sanimare':
                msg_special = 'val_usma'
            elif email_template_id == 'email_pfso':
                msg_special = 'val_pfso'
            elif email_template_id == 'email_pilot_moor':
                msg_special = 'val_pil_moor'
            elif email_template_id == 'email_tug':
                msg_special = 'val_tug'
            elif email_template_id == 'garbage_email':
                 msg_special = 'val_garbage'
            elif email_template_id == 'email_chemist':
                msg_special = 'val_chemist'
            elif email_template_id == 'email_gpg':
                msg_special = 'val_gpg'
            elif email_template_id == 'email_ens':
                msg_special = 'val_ens'
            elif email_template_id == 'email_garbage_cp':
                msg_special = 'val_garb_cp'
            elif email_template_id == 'email_integrazione_alim':
                msg_special = 'val_integr'
            elif email_template_id == 'email_chimico_cp':
                msg_special = 'ship_rec'
            elif email_template_id == 'not_rifiuti':
                msg_special = 'val_adsp'
            return msg_special
    
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
        if (email_to) is not None:
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
            msg_special='val_upd'
            return msg_special
       # print(x)

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
                msg_special='no_sof'
                return msg_special
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
        #verifichiamo che non mancano email destinatari TO e CCN altrimenti ritorniamo con la variabile msg_special che innesca il messaggio
        #verifichiamo se non presente l'email to allora inseriamo l'email del mittente
        if email_arr_to == email_arr_bcc == '':  
            msg_special = 'no_email'
            return msg_special
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
        #ritorniamo con la variabile msg_special per l'innesco del messaggio e il settaggio della checklist invio email a vero
        if email_template_id == 'email_updating_shiprec':
            msg_special = 'ship_rec_upd'
        else:
            msg_special = 'ship_rec'
        return msg_special

    @public_method
    def print_template(self, record, resultAttr=None, nome_template=None,  nome_vs=None, format_page=None, **kwargs):
        # Crea stampa
        
        tbl_arrival = self.db.table('shipsteps.arrival')
        builder = TableTemplateToHtml(table=tbl_arrival)
        #nome_template = nome_template #'shipsteps.arrival:check_list'

        nome_temp = nome_template.replace('shipsteps.arrival:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp +'_' + nome_vs)

        #nome_file_st = 'laboratorio_piazza_sta_{cl_id}.pdf'.format(
        #    cl_id=self.avatar.user_id)
        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)
       # print(x)
       #tbl_template=self.db.table('adm.htmltemplate')
       #letterhead = tbl_template.readColumns(columns='$id',
       #          where='$name=:tp_name', tp_name='A3_orizz')
        # (pdfpath.internal_path)
        if kwargs:
            letterhead=kwargs['letterhead_id']
        else:
            letterhead=''

        builder(record=record, template=template,letterhead_id=letterhead)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)
        #print(x)
        self.setInClientData(path='gnr.clientprint',
                             value=result.url(timestamp=datetime.now()), fired=True)

        return nome_temp

    @public_method
    def print_template_garbage(self, record, resultAttr=None,selId=None, nome_template=None, email_template_id=None,servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        selPkeys_att=kwargs['selPkeys_att']
        if selId is None:
            msg_special = 'yes'
            return msg_special

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
        self.email_services(record,email_template_id,servizio,selPkeys_att)
        #se ritorna il valore di self.msg_pecial dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di self.ms_special alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
        msg_special='val_garbage'
        return msg_special

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
