#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('sof_n',width='5em')
        r.fieldcell('nor_tend')
        r.fieldcell('nor_rec')
        r.fieldcell('nor_acc')
        r.fieldcell('ops_commenced')
        r.fieldcell('ops_completed')
        r.fieldcell('doc_onboard')
        r.fieldcell('ship_rec', width='40em')
        r.fieldcell('intestazione_sof')
        
    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')

class ViewFromSof(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('sof_n',width='3em')
        r.fieldcell('nor_tend', edit=True)
        r.fieldcell('nor_rec', edit=True)
        r.fieldcell('nor_acc', edit=True)
        r.fieldcell('ops_commenced', edit=True)
        r.fieldcell('ops_completed', edit=True)
        r.fieldcell('doc_onboard', edit=True)
        r.fieldcell('ship_rec')
        r.fieldcell('intestazione_sof', edit=True)

#class Form(BaseComponent):
#
#    def th_form(self, form):
#        pane = form.record
#        fb = pane.formbuilder(cols=2, border_spacing='4px')
#        fb.field('arrival_id')
#        fb.field('sof_n')
#        fb.field('nor_tend')
#        fb.field('nor_rec')
#        fb.field('nor_acc')
#        fb.field('ops_commenced')
#        fb.field('ops_completed')
#        fb.field('doc_onboard')
#        fb.field('int_sof')
        

class Form(BaseComponent):
    py_requires='gnrcomponents/pagededitor/pagededitor:PagedEditor'
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.datiSof(bc.roundedGroupFrame(title='Dati SOF',region='top',datapath='.record',height='110px', background='lightgrey', splitter=True))
        tc = bc.tabContainer(region = 'center',margin='2px')
        
        self.cargoSof(tc.contentPane(title='Cargo SOF'))
        self.operationsSof(tc.contentPane(title='SOF Operations'))

        tc_rem = tc.tabContainer(title='!![en]Remarks',margin='2px',tabPosition='left-h')#, region='center', height='450px', splitter=True)
        
        self.remarks_rs(tc_rem.contentPane(title='Receivers/Shippers Remarks',datapath='.record'))
        self.remarks_cte(tc_rem.contentPane(title='Master Remarks',datapath='.record'))
        self.remarks_note(tc_rem.contentPane(title='Note Remarks',datapath='.record'))
        self.onbehalf_remarks(tc_rem.contentPane(title='!![en]On behalf Sippers/Receivers',datapath='.record'))

        tc_tanks = tc.tabContainer(title='!![en]Tank times',margin='2px')
        self.tanks(tc_tanks.contentPane(title='Time tanks'))
        self.emailSof(tc.contentPane(title='Email SOF'))
        self.editSof(tc.framePane(title='Edit SOF', datapath='#FORM.editPagine'))
        self.Sofpdf(tc.framePane(title='SOF pdf', datapath='#FORM.pdf'))

    def datiSof(self,pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=4, border_spacing='4px',fld_width='10em')
        #fb.field('arrival_id')
        fb.field('sof_n', readOnly=True)
        fb.field('nor_tend')
        fb.field('nor_rec')
        fb.field('nor_acc')
        fb.field('ops_commenced')
        fb.field('ops_completed')
        fb.field('doc_onboard')
        fb.field('ship_rec', readOnly=True, width='30em',height='2em',colspan=2, tag='textArea')
        fb.field('onbehalf', width='15em', placeholder='insert the name of society')
        fb.field('int_sof', placeholder='eg.: Fiore Srl')
        
    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_sof,20,email_arrivo,20,email_operazioni,20,email_partenza,*,10')
        btn_sof_print=bar.stampa_sof.button('Print SOF')
        btn_sof_arrivo=bar.email_arrivo.button('Email arrival')
        btn_sof_oper=bar.email_operazioni.button('Email operations')
        btn_sof_partenza=bar.email_partenza.button('Email departure')
        btn_sof_print.dataRpc('nome_temp', self.print_sof,record='=#FORM.record',nome_template = 'shipsteps.sof:sof',format_page='A4')
        btn_sof_arrivo.dataRpc('nome_temp', self.email_sof,record='=#FORM.record',servizio=['arr','sof'], email_template_id='email_ormeggio',
                            nome_template = 'shipsteps.sof:email_ormeggio',format_page='A4',selPkeys_att='=#FORM/parent/#FORM.attachments.view.grid.currentSelectedPkeys',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        btn_sof_oper.dataRpc('nome_temp', self.email_sof,record='=#FORM.record',servizio=['arr','sof'], email_template_id='email_operations',
                            nome_template = 'shipsteps.sof:email_ormeggio',format_page='A4',selPkeys_att='=#FORM/parent/#FORM.attachments.view.grid.currentSelectedPkeys',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        btn_sof_partenza.dataRpc('nome_temp', self.email_sof,record='=#FORM.record',servizio=['arr','sof'], email_template_id='email_partenza',
                            nome_template = 'shipsteps.sof:email_ormeggio',format_page='A4',selPkeys_att='=#FORM/parent/#FORM.attachments.view.grid.currentSelectedPkeys',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        bar.dataController("""if(msgspec=='arrival_sof') genro.publish("floating_message",{message:msg_txt, messageType:"message"})""", msgspec='^nome_temp',msg_txt = 'Email ready to be sent')
        
    @public_method
    def print_sof(self, record, resultAttr=None, nome_template=None, format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        #print(x)
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special

        tbl_sof = self.db.table('shipsteps.sof')
        builder = TableTemplateToHtml(table=tbl_sof)

        nome_temp = nome_template.replace('shipsteps.sof:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        #builder(record=selId, template=template)
        builder(record=record_id, template=template)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)

    def cargoSof(self,pane):
        pane.inlineTableHandler(relation='@sof_cargo_sof',viewResource='ViewFromSof_Cargo',
                                picker='cargo_unl_load_id',
                                picker_condition='arrival_id=:aid',
                                picker_condition_aid='^#FORM.record.arrival_id',
                                picker_viewResource='ViewFromCargoLU_picker')

    def operationsSof(self,pane):
        pane.inlineTableHandler(relation='@sof_operations',viewResource='ViewFromSofOperations')

    

    def remarks_cte(self,frame):
        frame.simpleTextArea(title='!![en]Master Remarks',value='^.remarks_cte',editor=True)

    def remarks_note(self,frame):
        frame.simpleTextArea(title='!![en]Note / General Remarks',value='^.note',editor=True)

    def remarks_rs(self,frame):
        
        fb = frame.formbuilder(cols=1, border_spacing='4px',fld_width='50em', width='800px')
        fb.simpleTextArea(value='^.remarks_rs',editor=True, height='200px')
        fb.br()
        fb.button('Inserisci',lbl='Remark Wheat/Corn',action="""SET ^.remarks_rs = note_remark;
                                            alert("Inserito - Ricordati di salvare");""",
                    note_remark='=gnr.app_preference.shipsteps.remarks_wheat_corn')
    
    def onbehalf_remarks(self,frame):
        frame.simpleTextArea(value='^.onbehalf',editor=True)

    def tanks(self,pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=2, border_spacing='4px',fld_width='10em',table='shipsteps.sof_tanks',datapath='.record.@sof_tanks')
        fb.field('start_insp')
        fb.field('stop_insp')
        fb.field('cargo_calc')
        fb.br()
        fb.field('start_ullage')
        fb.field('stop_ullage')
        fb.field('hose_conn')
        fb.field('hose_disconn')
        fb.field('average')

    def emailSof(self,pane):
        pane.inlineTableHandler(title='Email SOF', relation='@sof_email',viewResource='ViewFromSofEmail')

    def editSof(self, frame):
        bar = frame.top.slotBar('10, lett_select,*',height='20px',border_bottom='1px solid silver')
        fb = bar.lett_select.formbuilder(cols=2,datapath='#FORM.record.htmlbag')
        fb.dbselect('^.letterhead_id',table='adm.htmltemplate',lbl='carta intestata',hasDownArrow=True)
        fb.button('Get Html Doc').dataRpc('#FORM.record.htmlbag.source',self.db.table('shipsteps.sof').getHTMLDoc,
                                            sof_id='=#FORM.pkey',
                                            record_template='sof',
                                            letterhead='.letterhead_id')
        
        frame.pagedEditor(value='^#FORM.record.htmlbag.source',pagedText='^#FORM.record.htmlbag.output',
                          border='1px solid silver',
                          letterhead_id='^#FORM.record.htmlbag.letterhead_id',
                          datasource='#FORM.record',printAction=True)
    def Sofpdf(self,frame):
        self.printDisplay(frame,resource='shipsteps.sof:html_res/sof_template')

    def printDisplay(self, frame, resource=None, html=None):
        bar = frame.top.slotBar('10,lett_select,*', height='20px', border_bottom='1px solid silver')
        bar.lett_select.formbuilder().dbselect('^.curr_letterhead_id',
                                                table='adm.htmltemplate',
                                                lbl='Carta intestata',
                                                hasDownArrow=True)
        frame.documentFrame(resource=resource,
                            pkey='^#FORM.pkey',
                            html=html,
                            letterhead_id='^.curr_letterhead_id',
                            missingContent='NO SOF',
                          _if='pkey',_delay=100)

    @public_method
    def email_sof(self, record,email_template_id=None,servizio=[],selPkeys_att=None, **kwargs):
        record_arr=record['arrival_id']
        
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
            sof_id=kwargs['record_attr']['_pkey']
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
                                                    where='$arrival_id=:a_id and $email_type=:type', a_id=record_arr,
                                                    type='to').fetch()
                for e in range(len(email_to)):
                    email_a_to.append(email_to[e][0])

                email_cc = tbl_email_arr.query(columns="$email",
                                                    where='$arrival_id=:a_id and $email_type=:type', a_id=record_arr,
                                                    type='cc').fetch()  
                for e in range(len(email_cc)):
                    email_a_cc.append(email_cc[e][0])

                email_bcc = tbl_email_arr.query(columns="$email",
                                                    where='$arrival_id=:a_id and $email_type=:type', a_id=record_arr,
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
        if email_template_id == 'email_ormeggio' or email_template_id == 'email_operations' or email_template_id == 'email_partenza':
            nome_temp = 'arrival_sof'
        
        return nome_temp

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
