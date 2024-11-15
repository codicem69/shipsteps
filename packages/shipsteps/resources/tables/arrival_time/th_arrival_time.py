#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('eosp', width='8em')
        r.fieldcell('aor', width='8em')
        r.fieldcell('anchored', width='8em')
        r.fieldcell('anchor_up', width='8em')
        r.fieldcell('pob', width='8em')
        r.fieldcell('first_rope', width='8em')
        r.fieldcell('moored', width='8em')
        r.fieldcell('poff', width='8em')
        r.fieldcell('gangway', width='8em')
        r.fieldcell('free_p', width='8em')
        r.fieldcell('pobd', width='8em')
        r.fieldcell('last_line', width='8em')
        r.fieldcell('sailed', width='8em')
        r.fieldcell('cosp', width='8em')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.arrival_details(bc)
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px')
        #fb.field('arrival_id' )
        #fb.field('eosp' )
        #fb.field('aor' )
        #fb.field('anchored' )
        #fb.field('anchor_up' )
        #fb.field('pob' )
        #fb.field('first_rope' )
        #fb.field('moored' )
        #fb.field('poff')
        #fb.field('gangway' )
        #fb.field('free_p' )
        #fb.field('pobd',border_color="^pildep") #tramite il datacontroller in th_sof viene assegnata alla variabile pildep il colore del bordo
        #fb.field('last_line' )
        #fb.field('sailed' ,border_color="^sail") #tramite il datacontroller in th_sof viene assegnata alla variabile sail il colore del bordo
        #fb.field('cosp' )
        #con il datacontroller all'inserimento dei dati in pobd e sailed risettiamo le variabili pildep e sail in null per togliere il colore rosso del bordo
        fb.dataController("""if(pobd!=null){SET pildep=null;} if(sailed!=null){SET sail=null;}""",pobd='^.pobd',sailed='^.sailed')
        btn_arrivo=fb.button('Email arrival',hidden="^checksof")#.controller.title?=#v!=null")
        btn_partenza=fb.button('Email departure',hidden="^checksof")#.controller.title?=#v!=null")
        fb.dataRpc('checksof', self.checkSof,  record='=#FORM.record', cur_tab='^#FORM/parent/#FORM.current_tab',
                   rec_id='=.id',pkey='^#FORM.record.id',_if="cur_tab==5||rec_id")

        btn_arrivo.dataRpc('nome_temp', self.email_arrdep,record='=#FORM.record',servizio=['arr'], email_template_id='email_arrivo',
                            nome_template = 'shipsteps.arrival:email_arrivo',format_page='A4',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        btn_partenza.dataRpc('nome_temp', self.email_arrdep,record='=#FORM.record',servizio=['arr'], email_template_id='email_departure',
                            nome_template = 'shipsteps.arrival:email_departure',format_page='A4',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))

    def arrival_details(self, bc):
        rg_times = bc.roundedGroup(title='!![en]Arrival/Departure times',table='shipsteps.arrival_time',region='left',datapath='.record',width='350px', height = 'auto').div(margin='10px',margin_left='2px')
        rg_details = bc.roundedGroup(title='!![en]Arrival details',table='shipsteps.arrival_det', region='center',datapath='.record.@arrival_id.@arr_details',width='350px', height = '100%',margin_left='350px').div(margin='10px',margin_left='2px')
        rg_details_dep = bc.roundedGroup(title='!![en]Departure details',table='shipsteps.arrival_det', region='center',datapath='.record.@arrival_id.@arr_details',width='350px', height = '100%',margin_left='350px').div(margin='10px',margin_left='2px')
        #rg_extra = bc.roundedGroup(title='!![en]Extra data CP on Arrival/Departure',table='shipsteps.extradaticp', region='center',datapath='.record.@extradatacp',width='auto', height = 'auto', margin_left='550px').div(margin='10px',margin_left='2px')
        fb = rg_times.formbuilder(cols=1, border_spacing='4px',fld_width='10em')
        fb.field('arrival_id', hidden=True)
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
        fb.field('pobd',border_color="^pildep") #tramite il datacontroller in th_sof viene assegnata alla variabile pildep il colore del bordo
        fb.field('last_line')
        fb.field('sailed',border_color="^sail") #tramite il datacontroller in th_sof viene assegnata alla variabile sail il colore del bordo
        fb.field('cosp', lbl='Commenced of <br>Sea Passage',fldvalign='center')
        
        btn_arrivo=fb.button('Email arrival',hidden="^checksof")#.controller.title?=#v!=null")
        btn_partenza=fb.button('Email departure',hidden="^checksof")#.controller.title?=#v!=null")
        fb.dataRpc('checksof', self.checkSof,  record='=#FORM.record', cur_tab='^#FORM.current_tab',titolo='^#FORM.controller.title',
                   _if='cur_tab!=null||titolo!=null')
        #con il datacontroller all'inserimento dei dati in pobd e sailed risettiamo le variabili pildep e sail in null per togliere il colore rosso del bordo
        fb.dataController("""if(pobd!=null){SET pildep=null;} if(sailed!=null){SET sail=null;}""",pobd='^.pobd',sailed='^.sailed')

        btn_arrivo.dataRpc('nome_temp', self.email_arrdep,record='=#FORM.record',servizio=['arr'], email_template_id='email_arrivo',
                            nome_template = 'shipsteps.arrival:email_arrivo',format_page='A4',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        btn_partenza.dataRpc('nome_temp', self.email_arrdep,record='=#FORM.record',servizio=['arr'], email_template_id='email_departure',
                            nome_template = 'shipsteps.arrival:email_departure',format_page='A4',
                            _ask=dict(title='!![en]Select the Attachments',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
        
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

    @public_method
    def checkSof(self, record, **kwargs):
        tabname=kwargs['cur_tab']
        record_id = record['arrival_id']
        tbl_sof = self.db.table('shipsteps.sof')
        sof = tbl_sof.query(columns='$id',where = '$arrival_id = :arr_id', arr_id=record_id).fetch()
        if sof:
            return True
        else:
            return False
    
    @public_method
    def email_arrdep(self, record,email_template_id=None,servizio=[],selPkeys_att=None, **kwargs):
        record_arr=record['id']
        arrival_id=record['id']
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
        
        #verifichiamo nei kwargs['template'] il valore assegnato dalla nostra scelta al lancio dell'email ossia l'email_template_id
        if 'template' in kwargs.keys():
            email_template_id=kwargs['template']

        #lettura degli attachmentTrue
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
        tbl_staff =  self.db.table('agz.staff')
        account_email,email_mittente = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('agz.agency')
        account_emailpec = tbl_agency.readColumns(columns='$emailpec_account_id',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

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
        #print(x)                                    
        self.db.table('email.message').newMessageFromUserTemplate(
                                                          record_id=record_arr,
                                                          table='shipsteps.arrival',
                                                          account_id = account_email,
                                                          to_address=email_arr_to,
                                                          cc_address=email_arr_cc,
                                                          bcc_address=email_arr_bcc,
                                                          attachments=attcmt,
                                                          template_code=email_template_id,
                                                          arrival_id=arrival_id)
        
        self.db.commit()
        #ritorniamo con la variabile nome_temp per l'innesco del messaggio e il settaggio della checklist invio email a vero
        #if email_template_id == 'email_ormeggio' or email_template_id == 'email_operations' or email_template_id == 'email_operations_mov' or email_template_id == 'email_partenza':
        if email_template_id != '' or email_template_id != None:
            nome_temp = 'val_upd'
            return nome_temp
            
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
