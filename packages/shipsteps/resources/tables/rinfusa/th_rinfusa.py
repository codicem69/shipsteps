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
        r.fieldcell('imb_sba')
        r.fieldcell('navigazione')
        r.fieldcell('doc_all', width='auto')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('imb_sba')
        fb.field('navigazione')
        fb.field('doc_all')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromRinfusa(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"
   #def th_form(self, form):
   #    pane = form.record
   #    fb = pane.formbuilder(cols=2, colswidth='20em', border_spacing='4px')
   #    #fb.field('arrival_id')
   #    fb.div('Select for Unloading otherwise leave deselected for Loading', colspan=2)
   #    fb.field('imb_sba',lbl='')
   #    fb.br()   
   #    fb.field('navigazione', validate_notnull=True)
   #    fb.br()
   #    fb.field('doc_all', tag='simpleTextArea', height='120px', colspan=2, width='50em', editor=True)
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.rinfusa_left(bc.contentPane(region='left',datapath='.record', width='50%',splitter=True))
        self.rinfusa_center(bc.contentPane(region='center'))
    
    def rinfusa_left(self,bc):
        left = bc.roundedGroup(title='Dati rinfusa',region='left')
        fb = left.formbuilder(cols=3, border_spacing='4px',fld_width='50em')
        #pane = form.record
        #fb = pane.formbuilder(cols=2, colswidth='20em', border_spacing='4px')
        #fb.field('arrival_id')
        #fb.div('Select for Unloading otherwise leave deselected for Loading', colspan=3)
        #fb.field('imb_sba',lbl='')
        fb.radioButtonText(value='^.imb_sba', values='True:Unloading,False:Loading', lbl='Cargo operations: ',validate_notnull=True) 
        fb.br()   
        fb.field('navigazione', validate_notnull=True, colspan=3)
        fb.br()
        fb.field('doc_all', tag='simpleTextArea', height='120px', colspan=3, editor=True)
    
    def rinfusa_center(self,pane):
        #center = pane.roundedGroup(title='Allegati rinfusa',region='center',width='50%')
        pane.attachmentGrid(viewResource='ViewFromRinfusa_atc')
       #fb = center.formbuilder(cols=2, border_spacing='4px')
       #fb.dock(id='mydock_1', position='relative')
       #
       #fb.paletteGrid(paletteCode='Attachments_Arrivals', dockTo='mydock_1',table='shipsteps.arrival_atc',viewResource='ViewFromArrivalAtc', datapath='shipsteps_arrival.form.shipsteps_rinfusa')
       #pg2 = fb.paletteGroup('Attachments_Vessel', dockTo='*', dockButton=True)
       #pg2.paletteGrid(paletteCode='Attachments_vessel',table='shipsteps.vessel_details_atc',viewResource='ViewFromVesselDocs',dockButton=True)
        #bar = fb.top.slotToolbar('*,palettetest,5')
        #bar.palettetest.paletteGrid(paletteCode='paletteprovincia',table='glbl.provincia',viewResource='View',dockButton=True)
   
    
    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_bulk_folder,stampa_bulk,email_bulk,*,10')
        btn_bulkfolder_print=bar.stampa_bulk_folder.button('Print Bulk folder')
        btn_bulk_print=bar.stampa_bulk.button('Print Bulk application')
        btn_bulk_email=bar.email_bulk.button('Email Bulk application')
        btn_bulkfolder_print.dataRpc('nome_temp', self.print_template_bulk,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.rinfusa:cartella_rinfusa',format_page='A3')
        btn_bulk_print.dataRpc('nome_temp', self.print_template_bulk,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.rinfusa:bulk_app',format_page='A4')
        #definiamo la tabella email_services per poi riprenderla sui dataRpc dei bottoni
        tbl_email_services = self.db.table('shipsteps.email_services')                            
        #verifichiamo quanti servizi CP ci sono, nel caso più di uno apparirà la dbSelect per la scelta
        service_for_email = tbl_email_services.query(columns="$service_for_email_id", where='$service_for_email_id=:serv', serv='cp').fetch()
        serv_len=len(service_for_email)
        if serv_len > 1:                    
            btn_bulk_email.dataRpc('nome_temp', self.print_template_bulk,record='=#FORM.record',record_arr='=#FORM/parent/#FORM.record',servizio=['capitaneria'], email_template_id='email_rinfusa_cp',
                                imbarcazione_id='=#FORM/parent/#FORM.record.@vessel_details_id.imbarcazione_id',nome_template = 'shipsteps.rinfusa:bulk_app',format_page='A4',
                                _ask=dict(title='!![en]Select the services',fields=[dict(name='services', lbl='!![en]Services', tag='dbSelect',hasDownArrow=True,
                                table='shipsteps.email_services', columns='$consignee', auxColumns='$email,$email_cc,$email_bcc,$email_pec,$email_cc_pec',condition="$service_for_email_id=:cod",condition_cod='cp',alternatePkey='consignee',
                                validate_notnull=True,cols=4,popup=True,colspan=2, hasArrowDown=True),dict(name='type_atc',lbl='!![en]Type atc',tag='filteringSelect',values='zip:zip,unzip:non compresso',default='unzip')]))
        else:
            btn_bulk_email.dataRpc('nome_temp', self.print_template_bulk,record='=#FORM.record',record_arr='=#FORM/parent/#FORM.record',servizio=['capitaneria'], email_template_id='email_rinfusa_cp',
                    imbarcazione_id='=#FORM/parent/#FORM.record.@vessel_details_id.imbarcazione_id',nome_template = 'shipsteps.rinfusa:bulk_app',format_page='A4',
                    _ask=dict(title='!![en]Select the services',fields=[dict(name='type_atc',lbl='!![en]Type atc',tag='filteringSelect',values='zip:zip,unzip:non compresso',default='unzip')]))                            
    
    @public_method
    def print_template_bulk(self, record, record_arr=None,imbarcazione_id=None, resultAttr=None, nome_template=None, email_template_id=None,servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special

        tbl_bulk = self.db.table('shipsteps.rinfusa')
        builder = TableTemplateToHtml(table=tbl_bulk)

        nome_temp = nome_template.replace('shipsteps.rinfusa:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id='istanza_rinfusa')

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        tbl_htmltemplate = self.db.table('adm.htmltemplate')
        templates= tbl_htmltemplate.query(columns='$id,$name', where='').fetch()
        letterhead=''       
        for r in range(len(templates)):
            if templates[r][1] == 'A4_vert':
                letterhead = templates[r][0]    
            if format_page=='A3':
                if templates[r][1] == 'A3_orizz':
                    letterhead = templates[r][0]
          
        builder(record=record_id, template=template,letterhead_id=letterhead)
        #builder(record=selId, template=template)
        #builder(record=record_id, template=template)
        #if format_page=='A3':
        #    builder.page_format='A3'
        #    builder.page_width=427
        #    builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)
        
        if email_template_id != '':
            agency_id = record_arr['agency_id']
            tbl_bolli = self.db.table('shipsteps.bolli')
            if record['imb_sba'] == 'True':
                note='sbarco'
            else:
                note='imbarco'   
            if not tbl_bolli.checkDuplicate(istanza='Istanza Rinfusa',ref_number=record_arr['reference_num'],id_istanza=record['id']):
                nuovo_record = dict(date=datetime.now(),imbarcazione_id=imbarcazione_id,istanza='Istanza Rinfusa',
                                id_istanza=record['id'],ref_number=record_arr['reference_num'],bolli_tr14=1,bolli_tr22=1,note=note,agency_id=agency_id)
                tbl_bolli.insert(nuovo_record) 
                self.db.commit()    

            self.email_services(record,email_template_id,servizio, **kwargs)
       
        #se ritorna il valore di self.msg_pecial dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di self.ms_special alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
            nome_temp='val_bulk'
            return nome_temp

    @public_method
    def email_services(self, record,email_template_id=None,servizio=[], **kwargs):
        arrival_id=record['arrival_id'] 
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

        tbl_att =  self.db.table('shipsteps.rinfusa_atc')
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
        
        #Condizioniamo l'aggiunta dell'allegato se il servizio invio email è il garbage
        if email_template_id=='email_rinfusa_cp':
            
            file_path = 'site:stampe_template/istanza_rinfusa.pdf'
            fileSn = self.site.storageNode(file_path)
            attcmt.append(fileSn.internal_path)
            attcmt_name.append(Path(fileSn.internal_path).name)

            pdfpath = self.site.storageNode('home:stampe_template')
            pdfpath=pdfpath.internal_path
            with zipfile.ZipFile(pdfpath + "/rinfusa.zip", mode="w") as archive:
               
                for filenamedir,filename in zip(attcmt,attcmt_name):
                     archive.write(filenamedir,filename)
                     #archive.write(pdfpath, basename(pdfpath))
        #file_path_zip = 'site:stampe_template/rinfusa.zip'
        
        #self.setInClientData(path='gnr.downloadurl',value=pdfpath,fired=True)
        #arch=archive.write(file_path_zip)
        
        
        # qui verfichiamo la variabile type_atc per la tipologia di allegati compressi o non per scegliere come allegarli all'email
        if type_atc == 'zip':
            attcmt=archive.filename #allegato zip
        elif type_atc == 'unzip':
            attcmt #allegato non zippato
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
                                                          template_code=email_template_id,
                                                          arrival_id=arrival_id)
            self.db.commit()

        if (email_pec_dest) is not None:
            self.db.table('email.message').newMessageFromUserTemplate(
                                                          record_id=record,
                                                          table='shipsteps.arrival',
                                                          account_id = account_emailpec,
                                                          to_address=email_pec,
                                                          cc_address=email_pec_cc,
                                                          attachments=attcmt,
                                                          template_code=email_template_id,
                                                          arrival_id=arrival_id)
            self.db.commit()
        
        
        if (email_dest or email_pec_dest) is not None:

          # if servizio == ['capitaneria']:
            
            return
            