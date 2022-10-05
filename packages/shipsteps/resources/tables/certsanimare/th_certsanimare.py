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
        r.fieldcell('xconto')
        r.fieldcell('docagent')
        r.fieldcell('doc_n')
        r.fieldcell('issuedby')
        r.fieldcell('datedoc')
        r.fieldcell('navigation')
        r.fieldcell('sanification')
        r.fieldcell('san_nsis')
        r.fieldcell('medicines')
        r.fieldcell('tab_medicine')
        r.fieldcell('med_nsis')
        r.fieldcell('waterbox')
        r.fieldcell('water_nsis')
        r.fieldcell('reg_narcotics')
        r.fieldcell('narcotics_nsis')
        r.fieldcell('newreg_narcotics')
        r.fieldcell('newnarcotics_nsis')
        r.fieldcell('destroy_med')
        r.fieldcell('destroymed_nsis')
        r.fieldcell('visit_date')
        r.fieldcell('date')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')

class ViewFromCertusma(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('xconto')
        r.fieldcell('docagent')
        r.fieldcell('doc_n')
        r.fieldcell('issuedby')
        r.fieldcell('datedoc')
        r.fieldcell('navigation')
        r.fieldcell('sanification')
        r.fieldcell('san_nsis')
        r.fieldcell('medicines')
        r.fieldcell('tab_medicine')
        r.fieldcell('med_nsis')
        r.fieldcell('waterbox')
        r.fieldcell('water_nsis')
        r.fieldcell('reg_narcotics')
        r.fieldcell('narcotics_nsis')
        r.fieldcell('newreg_narcotics')
        r.fieldcell('newnarcotics_nsis')
        r.fieldcell('destroy_med')
        r.fieldcell('destroymed_nsis')
        r.fieldcell('visit_date')
        r.fieldcell('date')

    def th_order(self):
        return 'arrival_id'

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('xconto')
        fb.field('docagent')
        fb.field('doc_n')
        fb.field('issuedby')
        fb.field('datedoc')
        fb.field('navigation')
        fb.field('sanification')
        fb.field('san_nsis')
        fb.field('medicines')
        fb.field('tab_medicine')
        fb.field('med_nsis')
        fb.field('waterbox')
        fb.field('water_nsis')
        fb.field('reg_narcotics')
        fb.field('narcotics_nsis')
        fb.field('newreg_narcotics')
        fb.field('newnarcotics_nsis')
        fb.field('destroy_med')
        fb.field('destroymed_nsis')
        fb.field('visit_date')
        fb.field('date')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromCertusma(BaseComponent):
    def th_form(self,form):
        pane = form.record
        
        fb = pane.formbuilder(cols=4, border_spacing='4px',fld_width='10em')
        fb.field('xconto',width='30em', placeholder='Es. comando nave M/V...', colspan=4)
        fb.br()  
        fb.field('docagent', placeholder="Es. Carta d'Identità")
        fb.field('doc_n')
        fb.field('issuedby', width='15em')
        fb.field('datedoc')
        fb.br()
        fb.field('navigation', width='30em', colspan=4)
        fb.br()
        div1=fb.div(width='99%',height='20%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='4px',colspan=4)
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
        fb2=pane.formbuilder(cols=9,colspan=9, border_spacing='4px',fld_width='10em')
        fb2.field('visit_date')
        fb2.field('date')

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_richiesta,email_richiesta,*,10')
        btn_cert_print=bar.stampa_richiesta.button('Print Certificate application')
        btn_cert_email=bar.email_richiesta.button('Email Certificate application')
        btn_cert_print.dataRpc('nome_temp', self.print_template_bulk,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.certsanimare:cert_sanimare',format_page='A4')
        btn_cert_email.dataRpc('nome_temp', self.print_template_bulk,record='=#FORM.record',servizio=['sanimare'], email_template_id='email_cert_sanimare',
                            nome_template = 'shipsteps.certsanimare:cert_sanimare',format_page='A4',_ask=dict(title='!![en]Select the Attachments',
                             fields=[dict(name='allegati_nave', lbl='!![en]Vessel Attachments', tag='checkboxtext',
                             table='shipsteps.vessel_details_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.vessel_details_id',width='22em',
                             cols=4,popup=True,colspan=2),dict(name='allegati', lbl='!![en]Arrival Attachments', tag='checkboxtext',
                             table='shipsteps.arrival_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM/parent/#FORM.record.id',
                             cols=4,popup=True,colspan=2)]))
       # bar.dataController("""if(msgspec=='certsanimare') {alert(msg_txt)};""",msgspec='^msg_special', msg_txt = 'Email ready to be sent')
        bar.dataController("""if(msgspec=='certsanimare') genro.publish("floating_message",{message:msg_txt, messageType:"message"});""",msgspec='^nome_temp', msg_txt = 'Email ready to be sent')
        
    @public_method
    def print_template_bulk(self, record, resultAttr=None, nome_template=None, email_template_id=None,servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        #print(x)
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special

        tbl_bulk = self.db.table('shipsteps.certsanimare')
        builder = TableTemplateToHtml(table=tbl_bulk)

        #nome_temp = nome_template.replace('shipsteps.certsanimare:','')
        
        nome_file = '{cl_id}.pdf'.format(
                    cl_id='istanza_sanimare')

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
        if email_template_id != '':
            self.email_services(record,email_template_id,servizio, **kwargs)
       
        #se ritorna il valore di self.msg_pecial dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di self.ms_special alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
            nome_temp='certsanimare'
            return nome_temp
    
    @public_method
    def email_services(self, record,email_template_id=None,servizio=[], **kwargs):
        id_rinfusa_atc=record['id']
        record=record['arrival_id']        
        if not record:
            return
        tbl_att =  self.db.table('shipsteps.rinfusa_atc')
        fileurl = tbl_att.query(columns='$fileurl',
                  where='$maintable_id=:mt_id',mt_id=id_rinfusa_atc).fetch()
        ln = len(fileurl)
        attcmt=[]
        attcmt_name=[]
        
        #trasformiamo la stringa pkeys allegati in una lista prelevandoli dai kwargs ricevuti tramite bottone
        #ma verifichiamo se nei kwargs gli allegati ci sono per non ritrovarci la variabile lista_all senza assegnazione
        
        for chiavi in kwargs.keys():
            if chiavi=='allegati':
                if kwargs['allegati']:
                    lista_all=list(kwargs['allegati'].split(","))
                else:
                    lista_all=None
            if chiavi=='allegati_nave':
                if kwargs['allegati_nave']:
                    lista_allnavi=list(kwargs['allegati_nave'].split(","))
                else:
                    lista_allnavi=None
    
        #lettura degli attachment arrival
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

        #lettura degli attachment doc navi
        if lista_allnavi:
            len_allegati = len(lista_allnavi) #verifichiamo la lunghezza della lista pkeys tabella allegati
            file_url=[]
            tbl_att =  self.db.table('shipsteps.vessel_details_atc') #definiamo la variabile della tabella allegati
            #ciclo for per la lettura dei dati sulla tabella allegati ritornando su ogni ciclo tramite la pkey dell'allegato la colonna $fileurl e alla fine
            #viene appesa alla variabile lista file_url
            for e in range(len_allegati):
                pkeys_att=lista_allnavi[e]
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
        
        
        #Condizioniamo l'aggiunta dell'allegato se il servizio invio email è sanimare
        if email_template_id=='email_cert_sanimare':
            
            file_path = 'site:stampe_template/istanza_sanimare.pdf'
            fileSn = self.site.storageNode(file_path)
            attcmt.append(fileSn.internal_path)

        
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
        email_d, email_cc_d,email_bcc_d, email_pec_d, email_pec_cc_d=[],[],[],[],[]

        tbl_email_services=self.db.table('shipsteps.email_services')
        for e in range(ln_serv):
            serv=servizio[e]

            email_dest, email_cc_dest,email_bcc_dest, email_pec_dest, email_pec_cc_dest = tbl_email_services.readColumns(columns="""$email,$email_cc,$email_bcc,$email_pec,$email_cc_pec""",
                                                    where='$service_for_email=:serv AND $agency_id=:ag_id', serv=serv,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'))
         
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
        email_to = ','.join([str(item) for item in email_d])
        email_cc = ','.join([str(item) for item in email_cc_d])
        email_bcc = ','.join([str(item) for item in email_bcc_d])
        email_pec = ','.join([str(item) for item in email_pec_d])
        email_pec_cc = ','.join([str(item) for item in email_pec_cc_d])
        
        if (email_dest) is not None:
            self.db.table('email.message').newMessageFromUserTemplate(
                                                          record_id=record,
                                                          table='shipsteps.arrival',
                                                          account_id = account_email,
                                                          to_address=email_to,
                                                          cc_address=email_cc,
                                                          bcc_address=email_bcc,
                                                          attachments=attcmt,
                                                          template_code=email_template_id)
            self.db.commit()

        if (email_pec_dest) is not None:
            self.db.table('email.message').newMessageFromUserTemplate(
                                                          record_id=record,
                                                          table='shipsteps.arrival',
                                                          account_id = account_emailpec,
                                                          to_address=email_pec,
                                                          cc_address=email_pec_cc,
                                                          attachments=attcmt,
                                                          template_code=email_template_id)
            self.db.commit()
        
        
        if (email_dest or email_pec_dest) is not None:

          # if servizio == ['capitaneria']:
            
            return