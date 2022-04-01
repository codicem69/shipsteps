#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
        r.fieldcell('cargo', width='50em')
        #r.fieldcell('@cargo_lu_arr.cargo_on_board', width='50em')
        r.fieldcell('cargo_lu_en', width='50em')
        r.fieldcell('@cargo_lu_arr.tot_cargo', width='10em')
        r.fieldcell('ship_rec', width='30em')

    def th_order(self):
        return 'agency_id'

    def th_query(self):
        return dict(column='reference_num', op='contains', val='')



class Form(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        #pane = form.record
        #fb = pane.formbuilder(cols=2, border_spacing='4px')

        bc1 = form.center.borderContainer()
        tc = bc1.tabContainer(margin='2px', region='center', height='auto', splitter=True)

        bc = tc.borderContainer(title='!![en]Arrival')
        bc_task = tc.borderContainer(title='!![en]Task List')
        tc_att = bc_task.tabContainer(margin='2px', region='center', height='auto')
        bc_task2 = tc.borderContainer(title='!![en]SOF')
       # tc2 = bc2.tabContainer(margin='2px', region='center', height='auto', splitter=True)
       # bc_top = bc.borderContainer(region='center',height='300px', splitter=True)
       # pane_center=bc_top.contentPane(region='center',datapath='.record', width='1200px', splitter=True)
        #pane_center=bc_top.contentPane(region='center',datapath='.record', width='1100px', splitter=True)
       # pane_right=bc_top.contentPane(region='right',datapath='.@gpg_arr', width='320px', splitter=True)
        self.datiArrivo(bc.borderContainer(region='top',height='300px', splitter=True, background = 'lavenderblush'))
        self.taskList(bc_task.borderContainer(title='!![en]Task list',region='top',height='50%', background = 'lavenderblush', splitter=True))
        self.sof(bc_task2.contentPane(title='!![en]Sof',height='100%'))
        #self.allegatiArrivo(tc_task.contentPane(title='Attachments', region='center', height='100%', splitter=True))
        self.allegatiArrivo(tc_att.contentPane(title='!![en]Attachments'))
        self.garbage(tc_att.contentPane(title='!![en]Garbage'))
        
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
        self.arrival_details(tc.borderContainer(title='!![en]Arrival details', region='top', background = 'lavenderblush'))
        self.emailArrival(tc.contentPane(title='!![en]Email Arrival'))
        #self.taskList(tc.borderContainer(title='!![en]Task list', region='top', background = 'lavenderblush'))

        #self.sof_cargo(tc_sof.contentPane(title='!![en]Sof_Cargo', datapath='.@sof_arr'))

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
        fb.field('vessel_details_id' )
        fb.field('pfda_id' , hasDownArrow=True,  auxColumns='$data,@imbarcazione_id.nome')
        fb.field('visit_id')

        fb = center1.formbuilder(cols=5, border_spacing='4px',lblpos='T',fldalign='left')
        fb.field('eta' , width='10em')
        fb.field('etb' , width='10em')
        fb.field('et_start' , width='10em')
        fb.field('etc' , width='10em')
        fb.field('ets', width='10em' )
        fb.field('draft_aft_arr', width='5em' )
        fb.field('draft_fw_arr' , width='5em')
        fb.field('draft_aft_dep' , width='5em')
        fb.field('draft_fw_dep' , width='5em')
        fb.field('dock_id' )
        fb.field('info_moor',width='30em', colspan=2 )
        fb.field('master_name' )
        fb.field('n_crew' , width='5em')
        fb.field('n_passengers' , width='5em')
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
        frame.simpleTextArea(title='!![en]Cargo on board',value='^.cargo_onboard',editor=True)

    def datiCarico(self,pane):
        pane.inlineTableHandler(relation='@cargo_lu_arr',viewResource='ViewFromCargoLU')

    def datiCaricoTransit(self,frame):
        frame.simpleTextArea(title='!![en]Transit cargo',value='^.transit_cargo',editor=True)

    def car_ric(self,pane):
        pane.inlineTableHandler(table='shipsteps.ship_rec',viewResource='ViewFromShipRec',view_store_onStart=True,export=True)

    def charterers(self,pane):
        pane.inlineTableHandler(table='shipsteps.charterers',viewResource='ViewFromCharterers',view_store_onStart=True,export=True)

    def sof(self,pane):
        pane.stackTableHandler(relation='@sof_arr', formResource='FormSof')

    def arrival_details(self, bc):
        rg_times = bc.roundedGroup(title='!![en]Arrival times',table='shipsteps.arrival_time',region='left',datapath='.record.@time_arr',width='350px', height = 'auto').div(margin='10px',margin_left='2px')
        rg_details = bc.roundedGroup(title='!![en]Arrival details',table='shipsteps.arrival_det', region='center',datapath='.record.@arr_details',width='auto', height = 'auto').div(margin='10px',margin_left='2px')

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

        fb = rg_details.formbuilder(cols=3, border_spacing='4px',fld_width='10em')

        #fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=3, border_spacing='4px',fld_width='10em',table='shipsteps.arrival_det',datapath='.record.@arr_details')
        fb.div('!![en]DRAFT')
        fb.br()
        fb.field('draft_aft_arr')
        fb.field('draft_fw_arr')
        fb.br()
        fb.field('draft_aft_dep')
        fb.field('draft_fw_dep')
        fb.br()
        fb.div('!![en]REMAINS')
        fb.br()
        fb.field('ifo_arr')
        fb.field('do_arr')
        fb.field('lo_arr')
        fb.field('ifo_dep')
        fb.field('do_dep')
        fb.field('lo_dep')
        fb.br()
        fb.div('FRESH WATER')
        fb.br()
        fb.field('fw_arr')
        fb.field('fw_dep')
        fb.br()
        fb.div('!![en]USED TUGS')
        fb.br()
        fb.field('tug_in')
        fb.field('tug_out')

    def emailArrival(self,pane):
        pane.inlineTableHandler(title='!![en]Email arrival',relation='@arrival_email',viewResource='ViewFromEmailArrival')
   #def sof_cargo(self,pane):
   #    pane.inlineTableHandler(table='shipsteps.sof_cargo', viewResource='ViewFromSof_Cargo')

    def taskList(self, bc_task):
        rg_prearrival = bc_task.roundedGroup(title='!![en]Pre arrival',table='shipsteps.tasklist',region='left',datapath='.record.@arr_tasklist',width='41%', height = '250px').div(margin='10px',margin_left='2px')
        rg_prearrival_cp = bc_task.roundedGroup(title='!![en]Pre arrival CP',table='shipsteps.tasklist',region='left',datapath='.record.@arr_tasklist',width='41%', height = 'auto',margin_top='250px').div(margin='10px',margin_left='2px')
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
        div1=rg_prearrival.div(width='96%',height='20%',margin='auto',
                        padding='5px',
                        border='1px solid silver',
                        margin_top='2px',margin_left='10px')
        fb1=div1.formbuilder(colspan=3,cols=9, border_spacing='4px')

        btn_cl = fb1.Button('!![en]Print')
        btn_cl.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id',
                            nome_template = 'shipsteps.arrival:check_list', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',format_page='A4')
        fb1.dataController("if(msg=='check_list') SET .checklist=true", msg='^nome_temp')
        fb1.field('checklist')
        fb1.semaphore('^.checklist')
        btn_fs = fb1.Button('!![en]Print')
        btn_fs.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:front_nave',format_page='A4')
        fb1.dataController("if(msg=='front_nave') SET .frontespizio=true", msg='^nome_temp')
        fb1.field('frontespizio')
        fb1.semaphore('^.frontespizio')

        btn_cn = fb1.Button('!![en]Print')
       #btn_cn.dataRpc(None, self.print_template,record='=#FORM.record.id',_ask=dict(title='!![en]Choose lettehead to use with this form',
       #                                        fields=[dict(name='letterhead_id', lbl='!![en]Letterhead', tag='dbSelect',columns='$id',
       #                                        hasDownArrow=True, auxColumns='$name', table='adm.htmltemplate')]), nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
       #                    nome_template = 'shipsteps.arrival:cartella_doc')
        btn_cn.dataRpc('nome_temp', self.print_template, record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:cartella_doc',format_page='A3')
        fb1.dataController("if(msg=='cartella_doc') SET .cartella_nave=true", msg='^nome_temp')
        fb1.field('cartella_nave')
        fb1.semaphore('^.cartella_nave')

        btn_ts = fb1.Button('!![en]Print')
        btn_ts.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:tab_servizi',format_page='A3')
        fb1.dataController("if(msg=='tab_servizi') SET .tab_servizi=true", msg='^nome_temp')
        fb1.field('tab_servizi')
        fb1.semaphore('^.tab_servizi')

        btn_fc = fb1.Button('!![en]Print')
        btn_fc.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:front_carico',format_page='A4')
        fb1.dataController("if(msg=='front_carico') SET .front_carico=true", msg='^nome_temp')
        fb1.field('front_carico')
        fb1.semaphore('^.front_carico')

        btn_mn = fb1.Button('!![en]Print',action="SET .modulo_nave=true")
        btn_mn.dataRpc('nome_temp', self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:mod_nave',format_page='A4')
        fb1.dataController("if(msg=='mod_nave') SET .checklist=true", msg='^nome_temp')
        fb1.field('modulo_nave')
        fb1.semaphore('^.modulo_nave')

        #definizione secondo rettangolo invio email all'interno del roundedGroup Pre Arrival
        div2=rg_prearrival.div(width='96%',height='20%',margin='auto',
                        padding='5px',
                        border='1px solid silver',
                        margin_top='2px',margin_left='10px')
        fb = div2.formbuilder(colspan=3,cols=9, border_spacing='4px')
        #fb = rg_prearrival.formbuilder(colspan=3,cols=6, border_spacing='4px',colswidth='10px')
        btn_dog = fb.Button('Email')
        btn_dog.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['dogana','gdf','gdf roan'], email_template_id='email_dogana')
        #datacontroller verifica il valore della variabile msg_special di ritorno dalla funzione per invio email
        #e setta il valore della campo checkbox a true e lancia il messaggio 'Messaggio Creato'
        fb.dataController("if(msgspec=='val_dog') {SET .email_dogana=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
        fb.field('email_dogana', lbl='!![en]Customs')
        fb.semaphore('^.email_dogana')

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

        btn_fr = fb.Button('Email')
        btn_fr.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['immigration'], email_template_id='email_frontiera')
        fb.dataController("if(msgspec=='val_imm') {SET .email_frontiera=true; alert('Messaggio Creato')}", msgspec='^msg_special')
        fb.field('email_frontiera',lbl='!![en]Immigration')
        fb.semaphore('^.email_frontiera')

        btn_usma = fb.Button('Email')
        btn_usma.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['sanimare'], email_template_id='email_sanimare')
        fb.dataController("if(msgspec=='val_usma') {SET .email_usma=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
        fb.field('email_usma', lbl='!![en]Sanimare')
        fb.semaphore('^.email_usma')

        btn_pfso = fb.Button('Email')
        btn_pfso.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['pfso'], email_template_id='email_pfso')
        fb.dataController("if(msgspec=='val_pfso') {SET .email_pfso=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
        fb.field('email_pfso', lbl='PFSO')
        fb.semaphore('^.email_pfso')

        btn_pilot = fb.Button('Email')
        btn_pilot.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['pilot','mooringmen'], email_template_id='email_pilot_moor')
        fb.dataController("if(msgspec=='val_pil_moor') {SET .email_pilot_moor=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
        fb.field('email_pilot_moor',lbl='Pilot/Moor')
        fb.semaphore('^.email_pilot_moor')

        btn_tug = fb.Button('Email')
        btn_tug.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['tug'], email_template_id='email_tug')
        fb.dataController("if(msgspec=='val_tug') {SET .email_tug=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
        #fb.dataController("alert(msg)", _if='msg',msg='^msg_special')
        fb.field('email_tug',lbl='!![en]Tug')
        fb.semaphore('^.email_tug')

        btn_garb = fb.Button('Email')
        btn_garb.dataRpc('msg_special', self.print_template_garbage,record='=#FORM.record.id',servizio=['garbage'], email_template_id='garbage_email',
                            nome_template = 'shipsteps.garbage:garbage_request',format_page='A4', selId='=shipsteps_arrival.form.shipsteps_garbage.view.grid.selectedId')
        #fb.dataController("alert(msg)", _if='msg',msg='^msg_select')
        fb.dataController("if(msgspec=='val_garbage') {SET .email_garbage=true ; alert('Messaggio Creato');} if(msgspec=='yes') alert('Devi selezionare il record del Garbage per la stampa'); "
                            , msgspec='^msg_special')

        fb.field('email_garbage',lbl='!![en]Garbage')
        fb.semaphore('^.email_garbage')

        btn_chem = fb.Button('Email')
        btn_chem.dataRpc('msg_special', self.email_services,
                   record='=#FORM.record.id', servizio=['chemist'], email_template_id='email_chemist')
        fb.dataController("if(msgspec=='val_chemist') {SET .email_chemist=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
        fb.field('email_chemist',lbl='!![en]Chemist')
        fb.semaphore('^.email_chemist')

        btn_gpg = fb.Button('Email')
        btn_gpg.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['gpg'], email_template_id='email_gpg')
        fb.dataController("if(msgspec=='val_gpg') {SET .email_gpg=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
        fb.field('email_gpg',lbl='GPG')
        fb.semaphore('^.email_gpg')

        btn_ens = fb.Button('Email')
        btn_ens.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['ens'], email_template_id='email_ens')
        fb.dataController("if(msgspec=='val_ens') {SET .email_ens=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
       # fb.dataController('SET .email_ens=True',__if='msg',msg='^msg_special')
        fb.field('email_ens',lbl='ENS')
        fb.semaphore('^.email_ens')
        btn_af = fb.Button('Email')
        fb.field('email_antifire', lbl='!![en]Antifire')
        fb.semaphore('^.email_antifire')

        #definizione terzo rettangolo dentro rounded Group Pre Arrival CP
        div_cp=rg_prearrival_cp.div(width='96%',height='60%',margin='auto',
                        padding='5px',
                        border='1px solid silver',
                        margin_top='2px',margin_left='10px')
        fb_cp=div_cp.formbuilder(colspan=3,cols=9, border_spacing='4px')
        
        btn_integr = fb_cp.Button('Email')
        btn_integr.dataRpc('msg_special', self.email_services,
                  record='=#FORM.record.id', servizio=['capitaneria'], email_template_id='email_integrazione_alim')
        fb_cp.dataController("if(msgspec=='val_integr') {SET .email_integr=true ; alert('Messaggio Creato')}", msgspec='^msg_special')
       # fb.dataController('SET .email_ens=True',__if='msg',msg='^msg_special')
        fb_cp.field('email_integr', lbl='!![en]Alimentary integration')
        fb_cp.semaphore('^.email_integr')

    def allegatiArrivo(self,pane):
        pane.attachmentGrid(viewResource='ViewFromArrivalAtc')

    def garbage(self, pane):
        pane.inlineTableHandler(relation='@garbage_arr',viewResource='ViewFromGarbage')
    

    @public_method
    def email_services(self, record,email_template_id=None,servizio=[], **kwargs):
        tbl_arrival = self.db.table('shipsteps.arrival')

        
        if not record:
            return
        tbl_att =  self.db.table('shipsteps.arrival_atc')
        fileurl = tbl_att.query(columns='$fileurl',
                  where='$att_email=:a_att AND $maintable_id=:mt_id',
                    a_att='true',mt_id=record).fetch()
        ln = len(fileurl)
        attcmt=[]
       # a=0
       # r=1
        for r in range(ln):
            file_url = fileurl[r][0]
            file_path = file_url.replace('/home','site')
            fileSn = self.site.storageNode(file_path)
            attcmt.append(fileSn.internal_path)

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

            if servizio == ['dogana','gdf','gdf roan']:
                msg_special = 'val_dog'
            elif servizio == ['immigration']:
                msg_special = 'val_imm'
            elif servizio == ['sanimare']:
                msg_special = 'val_usma'
            elif servizio == ['pfso']:
                msg_special = 'val_pfso'
            elif servizio == ['pilot','mooringmen']:
                msg_special = 'val_pil_moor'
            elif servizio == ['tug']:
                msg_special = 'val_tug'
            elif servizio == ['garbage']:
                 msg_special = 'val_garbage'
            elif servizio == ['chemist']:
                msg_special = 'val_chemist'
            elif servizio == ['gpg']:
                msg_special = 'val_gpg'
            elif servizio == ['ens']:
                msg_special = 'val_ens'
            elif servizio == ['capitaneria']:
                msg_special = 'val_integr'
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
        self.email_services(record,email_template_id,servizio)
        #se ritorna il valore di self.msg_pecial dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di self.ms_special alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
        msg_special='val_garbage'
        return msg_special

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
