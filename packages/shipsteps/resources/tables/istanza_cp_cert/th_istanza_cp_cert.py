#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
import zipfile
import os
from os.path import basename
from pathlib import Path

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('data_visita')
        r.fieldcell('contatto')
        r.fieldcell('perconto')
        r.fieldcell('registro_classe')
        r.fieldcell('certificato')
        r.fieldcell('navigazione')
        r.fieldcell('servizio')
        r.fieldcell('motivo_istanza')
        r.fieldcell('note')
     

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('data_visita')
        fb.field('contatto')
        fb.field('perconto')
        fb.field('registro_classe')
        fb.field('certificato')
        fb.field('navigazione')
        fb.field('servizio')
        fb.field('motivo_istanza')
        fb.field('note')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromCertificates(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"
   
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.certificates_left(bc.contentPane(region='left',datapath='.record', width='50%',splitter=True))
        self.certificates_center(bc.contentPane(region='center'))

    
    def certificates_left(self,bc):
        left = bc.roundedGroup(title='Dati Istanza',region='left', height = 'auto').div(margin='10px',margin_left='2px')
        fb = left.formbuilder(cols=2, border_spacing='4px')
        fb.div("""a) Le istanze finalizzate al rilascio/rinnovo/convalida del Documento di Conformità (ISM DOC) e del Certificato gestione sicurezza (ISM/SMC) DEVONO essere 
                     corredate dall’allegato A.1 debitamente compilato.""", colspan=2)
        fb.br()                     
        fb.div("""b) Le istanze finalizzate al rilascio/rinnovo/convalida del ISSC (sia provvisorio che definitivo) POSSONO essere presentate dall’Agenzia marittima raccomandataria 
                         della nave, FERMO RESTANDO l’obbligo per la Società di gestione di provvedere alla consegna della documentazione richiesta nei tempi e secondo le modalità previste 
                         dalle disposizioni di legge vigenti in materia.""", colspan=2)
        fb.br()
        fb.field('data_visita')
        fb.field('contatto', placeholder='Inserire numero telefonico da contattare', width='30em')
        fb.field('perconto', placeholder='in qualità di / in nome e per conto di', colspan=2, width='100%')
        fb.field('registro_classe', placeholder='Nome registro di classe', colspan=2 ,width='100%')
        fb.field('certificato', colspan=2, width='100%')
        fb.field('navigazione', placeholder='Tipo di navigazione abilitata', colspan=2, width='100%')
        fb.field('servizio',colspan=2 , width='100%')
        fb.radioButtonText(value='^.motivo_istanza', values='Rilascio:Rilascio,Rinnovo:Rinnovo,convalida per visita periodica:Visita periodica, convalida per visita occasionale:Visita occasionale', 
                           lbl='!![en]Reason for application: ',validate_notnull=True, colspan=2, width='100%') 
        fb.field('note', tag='simpleTextArea',editor=True, height='50px', colspan=2, width='100%', placeholder='inserire informazioni utili a riguardo del certificato/provvedimento richiesto')
        fb.div('ALLEGATI', font_weight='bold',colspan=2)
        fb.div("""Inserire ad esempio:<br>n.1 marca da bollo da € 16,00;<br>n.1 Attestazione di versamento di € xx,xx eseguito sul C/C 123456 Capo XV Capitolo 2170
                   intestato a Tesoreria Provinciale dello Stato Chieti;<br>n.1 Scheda nave (in caso di istanze tese ad ottenere autorizzazioni/deroghe/esenzioni
                   da parte del Comando del Corpo del le Capitanerie di Porto""", colspan=2, width='100%')
        fb.field('allegati', tag='simpleTextArea', editor=True, height='100px', colspan=2, width='100%')
        #fb.simpleTextArea(title='!![en]Attachments',value='^.allegati', width='50em', height='100px')    
      
        
    def certificates_center(self,pane):
        pane.attachmentGrid(viewResource='ViewFromCertificates_atc')  

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_folder,stampa_istanza,email_istanza,*,10')
        btn_folder_print=bar.stampa_folder.button('Print folder')
        btn_istanza_print=bar.stampa_istanza.button('Print application')   
        btn_istanza_email=bar.email_istanza.button('Email Certificate application')
        btn_folder_print.dataRpc('nome_temp', self.print_template_istanzacert,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.istanza_cp_cert:cartella_istanza',format_page='A3')
        btn_istanza_print.dataRpc('nome_temp', self.print_template_istanzacert,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.istanza_cp_cert:certificate_app',format_page='A4') 
         #definiamo la tabella email_services per poi riprenderla sui dataRpc dei bottoni
        tbl_email_services = self.db.table('shipsteps.email_services')                            
        #verifichiamo quanti servizi CP ci sono, nel caso più di uno apparirà la dbSelect per la scelta
        service_for_email = tbl_email_services.query(columns="$service_for_email_id", where='$service_for_email_id=:serv', serv='cp').fetch()
        serv_len=len(service_for_email)
        if serv_len > 1:                    
            btn_istanza_email.dataRpc('nome_temp', self.print_template_istanzacert,record='=#FORM.record',servizio=['capitaneria'], email_template_id='email_certificate_cp',
                                nome_template = 'shipsteps.istanza_cp_cert:certificate_app',format_page='A4',
                                _ask=dict(title='!![en]Select the services',fields=[dict(name='services', lbl='!![en]Services', tag='dbSelect',hasDownArrow=True,
                                table='shipsteps.email_services', columns='$consignee', auxColumns='$email,$email_cc,$email_bcc,$email_pec,$email_cc_pec',condition="$service_for_email_id=:cod",condition_cod='cp',alternatePkey='consignee',
                                validate_notnull=True,cols=4,popup=True,colspan=2, hasArrowDown=True),dict(name='type_atc',lbl='!![en]Type atc',tag='filteringSelect',values='zip:zip,unzip:non compresso')]))
        else:
            btn_istanza_email.dataRpc('nome_temp', self.print_template_istanzacert,record='=#FORM.record',servizio=['capitaneria'], email_template_id='email_certificate_cp',
                    nome_template = 'shipsteps.istanza_cp_cert:certificate_app',format_page='A4',
                    _ask=dict(title='!![en]Select the services',fields=[dict(name='type_atc',lbl='!![en]Type atc',tag='filteringSelect',values='zip:zip,unzip:non compresso')]))         

    @public_method
    def print_template_istanzacert(self, record, resultAttr=None, nome_template=None, email_template_id=None,servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        #print(x)
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special
        
        tbl_istanzacert = self.db.table('shipsteps.istanza_cp_cert')
        builder = TableTemplateToHtml(table=tbl_istanzacert)

        nome_temp = nome_template.replace('shipsteps.istanza_cp_cert:','')
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
        if email_template_id != '':
            self.email_services(record,email_template_id,servizio, **kwargs)
       
        #se ritorna il valore di self.msg_pecial dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di self.ms_special alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
            nome_temp='val_bulk'
            return nome_temp

    @public_method
    def email_services(self, record,email_template_id=None,servizio=[], **kwargs):
        
        id_rinfusa_atc=record['id']
        record=record['arrival_id']        
        if not record:
            return
        #leggiamo nei kwargs la tipologia dell'allegato se zip oppure non compresso
        type_atc = None
        for chiavi in kwargs.keys():    
            if chiavi=='type_atc':
                if kwargs['type_atc']:
                    type_atc=kwargs['type_atc']   

        tbl_att =  self.db.table('shipsteps.istanza_cp_cert_atc')
        fileurl = tbl_att.query(columns='$fileurl',
                  where='$maintable_id=:mt_id',mt_id=id_rinfusa_atc).fetch()
        ln = len(fileurl)
        attcmt=[]
        attcmt_name=[]
        
        for r in range(ln):
            file_url = fileurl[r][0]
            file_path = file_url.replace('/home','site')
            fileSn = self.site.storageNode(file_path)
            attcmt.append(fileSn.internal_path)
            attcmt_name.append(Path(fileSn.internal_path).name)
        
        #Condizioniamo l'aggiunta dell'allegato se il servizio invio email è l'istanza per i certificati
        if email_template_id=='email_certificate_cp':
            
            file_path = 'site:stampe_template/certificate_app.pdf'
            fileSn = self.site.storageNode(file_path)
            attcmt.append(fileSn.internal_path)
            attcmt_name.append(Path(fileSn.internal_path).name)

            pdfpath = self.site.storageNode('home:stampe_template')
            pdfpath=pdfpath.internal_path
            with zipfile.ZipFile(pdfpath + "/istanza.zip", mode="w") as archive:
               
                for filenamedir,filename in zip(attcmt,attcmt_name):
                     archive.write(filenamedir,filename)
                     #archive.write(pdfpath, basename(pdfpath))
        #file_path_zip = 'site:stampe_template/rinfusa.zip'
        
        #self.setInClientData(path='gnr.downloadurl',value=pdfpath,fired=True)
        #arch=archive.write(file_path_zip)
        
        if type_atc == 'zip':
            attcmt=archive.filename
        elif type_atc == 'unzip':
            attcmt
        else:
            attcmt=archive.filename  
           #if r < (ln-1):
           #    attcmt = attcmt + fileSn.internal_path + ','
           #else:
           #    attcmt = attcmt + fileSn.internal_path
        
        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('agz.staff')
        account_email = tbl_staff.readColumns(columns='$email_account_id',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('agz.agency')
        account_emailpec = tbl_agency.readColumns(columns='$emailpec_account_id',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        #leggiamo nei kwargs il servizio richiesto per invio email
        services = None
        for chiavi in kwargs.keys():
            if chiavi=='services':
                if kwargs['services']:
                    services=kwargs['services']
                 
        #Lettura degli indirizzi email destinatari
        ln_serv=len(servizio)
        #definiamo le tabelle su cui effettuare le ricerche
        tbl_emailservices = self.db.table('shipsteps.email_services')
        #preleviamo il nome esatto del servizio service_for_email_id
        service_for_email_id = tbl_emailservices.readColumns(columns="$service_for_email_id", where='$service_for_email=:serv AND $consignee=:cons', serv=servizio[0], cons=services)
        #aggiorniamo a true la colonna default del servizio richiesto
        tbl_emailservices.batchUpdate(dict(default=True),
                                    where='$consignee=:cons', cons=services)                         
        #aggiorniamo a false la colonna default degli eventuali servizi aggiunti non richiesti
        tbl_emailservices.batchUpdate(dict(default=False),
                                    where='$consignee != :cons AND $service_for_email_id =:servizio',cons=services, servizio=service_for_email_id)  
                                                                  
        self.db.commit()
        #email_d, email_cc_d, email_pec_d, email_pec_cc_d=[],[],[],[]
        email_d, email_cc_d,email_bcc_d, email_pec_d, email_pec_cc_d=[],[],[],[],[]
        #print(x)
        tbl_email_services=self.db.table('shipsteps.email_services')
        for e in range(ln_serv):
            serv=servizio[e]

            email_dest, email_cc_dest,email_bcc_dest, email_pec_dest, email_pec_cc_dest = tbl_email_services.readColumns(columns="""$email,$email_cc,$email_bcc,$email_pec,$email_cc_pec""",
                                                    where='$service_for_email=:serv AND $agency_id=:ag_id AND $consignee=:cons', serv=serv,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'), cons=services)
         
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