#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id', width='7em')
        r.fieldcell('reference_num', width='7em')
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
       # tc2 = bc2.tabContainer(margin='2px', region='center', height='auto', splitter=True)
       # bc_top = bc.borderContainer(region='center',height='300px', splitter=True)
       # pane_center=bc_top.contentPane(region='center',datapath='.record', width='1200px', splitter=True)
        #pane_center=bc_top.contentPane(region='center',datapath='.record', width='1100px', splitter=True)
       # pane_right=bc_top.contentPane(region='right',datapath='.@gpg_arr', width='320px', splitter=True)
        self.datiArrivo(bc.borderContainer(region='top',height='300px', splitter=True, background = 'lavenderblush'))
        self.taskList(bc_task.borderContainer(title='!![en]Task list',region='top',height='50%', background = 'lavenderblush'))
        self.allegatiArrivo(bc_task.contentPane(title='Attachments', region='center', height='50%'))
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
        self.sof(tc.contentPane(title='!![en]Sof'))
        self.arrival_details(tc.borderContainer(title='!![en]Arrival details', region='top', background = 'lavenderblush'))
        self.emailArrival(tc.contentPane(title='!![en]Email Arrival'))
        #self.taskList(tc.borderContainer(title='!![en]Task list', region='top', background = 'lavenderblush'))
        
        #self.sof_cargo(tc_sof.contentPane(title='!![en]Sof_Cargo', datapath='.@sof_arr'))

    def datiArrivo(self,bc):
        center = bc.roundedGroup(title='!![en]Vessel arrival', region='center',datapath='.record',width='210px', height = '100%').div(margin='10px',margin_left='2px')
        center1 = bc.roundedGroup(title='!![en]Arrival details',region='center',datapath='.record',width='960px', height = '100%', margin_left='210px').div(margin='10px',margin_left='2px')
        center2 = bc.roundedGroup(title='!![en]Special security guards',table='shipsteps.gpg',region='center',datapath='.record.@gpg_arr',width='215px', height = '100%', margin_left='1170px').div(margin='10px',margin_left='2px')
        #center3 = bc.roundedGroup(title='!![en]Times',table='shipsteps.arrival_time',region='center',datapath='.record.@time_arr',width='245px', height = '350px', margin_left='1385px').div(margin='10px',margin_left='2px')

        fb = center.formbuilder(cols=1, border_spacing='4px',lblpos='T')   
        fb.field('agency_id', readOnly=True )
        fb.field('reference_num', readOnly=True)
        fb.field('date')
        fb.field('vessel_details_id' )
        fb.field('pfda_id' , hasDownArrow=True,  auxColumns='$data,@imbarcazione_id.nome')

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
        fb.field('mandatory', colspan=2 , width='30em')
        fb.field('cargo_dest', colspan=2, width='30em' )
        fb.br()
        fb.field('invoice_det_id',colspan=5 ,width='78em', hasDownArrow=True)
        
        fb = center2.formbuilder(cols=1, border_spacing='4px', fld_width='8em')
        #fb.field('arrival_id')
        fb.field('date_start')
        fb.field('date_end')
        fb.field('n_gpg')
        
        
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
        pane.dialogTableHandler(table='shipsteps.ship_rec',view_store_onStart=True,export=True)

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
        rg_prearrival = bc_task.roundedGroup(title='!![en]Pre arrival',table='shipsteps.tasklist',region='left',datapath='.record.@arr_tasklist',width='700px', height = 'auto').div(margin='10px',margin_left='2px')
        #rg_details = bc.roundedGroup(title='!![en]Arrival details',table='shipsteps.arrival_det', region='center',datapath='.record.@arr_details',width='auto', height = 'auto').div(margin='10px',margin_left='2px')
        tbl_staff =  self.db.table('shipsteps.staff')
        account_email = tbl_staff.readColumns(columns='$email_account_id',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

        fb = rg_prearrival.formbuilder(colspan=3,cols=6, border_spacing='4px')#,fld_width='10em')
        #fb.field('arrival_id')
        btn_cl = fb.Button('!![en]Print')
        btn_cl.dataRpc(None, self.print_template,record='=#FORM.record.id',
                            nome_template = 'shipsteps.arrival:check_list', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome')
        fb.field('cheklist')
        fb.semaphore('^.cheklist')

        btn_fs = fb.Button('!![en]Print')
        btn_fs.dataRpc(None, self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:front_nave')
        fb.field('frontespizio')
        fb.semaphore('^.frontespizio')

        btn_cn = fb.Button('!![en]Print')
        btn_cn.dataRpc(None, self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:cartella_doc')
        fb.field('cartella_nave')
        fb.semaphore('^.cartella_nave')

        btn_ts = fb.Button('!![en]Print')
        btn_ts.dataRpc(None, self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:tab_servizi')
        fb.field('tab_servizi')
        fb.semaphore('^.tab_servizi')

        btn_fc = fb.Button('!![en]Print')
        btn_fc.dataRpc(None, self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:front_carico')
        fb.field('front_carico')
        fb.semaphore('^.front_carico')

        btn_mn = fb.Button('!![en]Print')
        btn_mn.dataRpc(None, self.print_template,record='=#FORM.record.id', nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome',
                            nome_template = 'shipsteps.arrival:mod_nave')
        fb.field('modulo_nave')
        fb.semaphore('^.modulo_nave')
    
        btn_dog = fb.Button('Email')
        btn_dog.dataRpc(None, self.email_dog_gdf,
                   record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_dogana')
        fb.field('email_dogana')
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
        btn_fr.dataRpc(None, self.email_dog_gdf,
                   record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_frontiera')
        fb.field('email_frontiera')
        fb.semaphore('^.email_frontiera')

        btn_usma = fb.Button('Email')
        btn_usma.dataRpc(None, self.email_dog_gdf,
                   record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_sanimare')
        fb.field('email_usma')
        fb.semaphore('^.email_usma')

        btn_pfso = fb.Button('Email')
        btn_pfso.dataRpc(None, self.email_dog_gdf,
                   record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_pfso')
        fb.field('email_pfso')
        fb.semaphore('^.email_pfso')

        btn_pilot = fb.Button('Email')
        btn_pilot.dataRpc(None, self.email_dog_gdf,
                   record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_pilot_moor')
        fb.field('email_pilot_moor')
        fb.semaphore('^.email_pilot_moor')

        btn_tug = fb.Button('Email')
        btn_tug.dataRpc(None, self.email_dog_gdf,
                   record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_tug')
        fb.field('email_tug')
        fb.semaphore('^.email_tug')

        btn_garb = fb.Button('Email')
       #btn_garb.dataRpc(None, self.email_dog_gdf,
       #           record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_garbage')
        fb.field('email_garbage')
        fb.semaphore('^.email_garbage')

        btn_chem = fb.Button('Email')
        btn_chem.dataRpc(None, self.email_dog_gdf,
                   record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_chemist')
        fb.field('email_chemist')
        fb.semaphore('^.email_chemist')
                
        btn_gpg = fb.Button('Email')
       #btn_gpg.dataRpc(None, self.email_dog_gdf,
       #           record='=#FORM.record.id', email_account_id=account_email, email_template_id='email_gpg')
        fb.field('email_gpg')
        fb.semaphore('^.email_gpg')

        btn_ens = fb.Button('Email')
        fb.field('email_ens')
        fb.semaphore('^.email_ens')
        btn_af = fb.Button('Email')
        fb.field('email_antifire')
        fb.semaphore('^.email_antifire')
    def allegatiArrivo(self,pane):
        pane.attachmentGrid(viewResource='ViewFromArrivalAtc')

    @public_method
    def email_dog_gdf(self, record,email_account_id,email_template_id, **kwargs):
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
           #if r < (ln-1):
           #    attcmt = attcmt + fileSn.internal_path + ',' 
           #else: 
           #    attcmt = attcmt + fileSn.internal_path
                
                 
        self.db.table('email.message').newMessageFromUserTemplate(
                                                      record_id=record,
                                                      table='shipsteps.arrival',
                                                      account_id = email_account_id,
                                                      attachments=attcmt,
                                                      template_code=email_template_id)
        
        self.db.commit()
        
    @public_method
    def print_template(self, record, resultAttr=None, nome_template=None,  nome_vs=None, **kwargs):
        # Crea stampa
       # if not record['datarisultato']:
        #    return
        
        tbl_arrival = self.db.table('shipsteps.arrival')
        builder = TableTemplateToHtml(table=tbl_arrival)
        #nome_template = nome_template #'shipsteps.arrival:check_list'
        #print(x)
        nome_temp = nome_template.replace('shipsteps.arrival:','')    
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp +'_' + nome_vs)
        
        #nome_file_st = 'laboratorio_piazza_sta_{cl_id}.pdf'.format(
        #    cl_id=self.avatar.user_id)
        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)
        
        # (pdfpath.internal_path)
        builder(record=record, template=template)
        result = builder.writePdf(pdfpath=pdfpath)
       
        self.setInClientData(path='gnr.clientprint',
                             value=result.url(timestamp=datetime.now()), fired=True)
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
