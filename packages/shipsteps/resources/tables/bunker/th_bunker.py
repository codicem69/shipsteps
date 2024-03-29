#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
import re,os
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
import zipfile
import os
from os.path import basename
from pathlib import Path

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('arrival_id')
        r.fieldcell('rank_off')
        r.fieldcell('name_off')
        r.fieldcell('datetime_bunk')
        r.fieldcell('service')
        r.fieldcell('durata')
        r.fieldcell('ditta_trasp')
        r.fieldcell('iscr_dt')
        r.fieldcell('lg_ditta_transp')
        r.fieldcell('email_transp')
        r.fieldcell('ditta_forn')
        r.fieldcell('iscr_forn')
       

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('rank_off')
        fb.field('name_off')
        fb.field('datetime_bunk')
        fb.field('service')
        fb.field('durata')
        fb.field('ditta_trasp')
        fb.field('iscr_dt')
        fb.field('lg_ditta_transp')
        fb.field('email_transp')
        fb.field('ditta_forn')
        fb.field('iscr_forn')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromBunker(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        #bc = tc.borderContainer(title='Form')
        self.bunkerTestata(bc.borderContainer(region='top',datapath='.record',height='200px'))
        self.bunkerRighe(bc.contentPane(region='center'))
        self.bunker_att(bc.contentPane(region='right',width='50%'))

    def bunkerTestata(self,bc):    
        center = bc.roundedGroup(title='!![en]Bunker details',region='center',width='auto')
        fb = center.formbuilder(cols=4, border_spacing='4px')
        #fb.field('arrival_id')
        fb.field('datetime_bunk')
        fb.field('rank_off')
        fb.field('name_off')
        fb.field('service')
        fb.field('durata')
        fb.field('ditta_trasp')
        fb.field('iscr_dt')
        fb.br()
        fb.field('lg_ditta_transp')
        fb.field('email_transp')
        fb.field('ditta_forn')
        fb.field('iscr_forn')
        fb.br()
        fb.dbSelect(dbtable='shipsteps.invoice_det',lbl='Select Invoice',auxColumns='$fullname',
                    selected_fullname='.dati_fatt',condition="$id =:cod",condition_cod='=#FORM/parent/#FORM.record.invoice_det_id',
                        hasDownArrow=True)
        fb.field('dati_fatt',colspan=3, width='72em')
        fb.br()
        fb.field('invio_fatt', placeholder='Insert the fullstyle where to send the invoice in case is different than your Agency', colspan=4, width='69em')
        
        right = bc.roundedGroup(title='!![en]Transportation Company stamp', region='right', width='250px')
        right.img(src='^.stamp_transp', edit=True, crop_width='250px', crop_height='150px', 
                        placeholder=True, upload_folder='site:application', upload_filename='=.id')
        right.button('!![en]Remove image', hidden='^.stamp_transp?=!#v').dataRpc(self.deleteImage, image='=.stamp_transp')

    def bunker_att(self,pane):
        #center = pane.roundedGroup(title='Allegati rinfusa',region='center',width='50%')
        pane.attachmentGrid(viewResource='ViewFromBunker_atc')

    def bunkerRighe(self,bc):
        left = bc.contentPane(region='center',width='500px', datapath='#FORM')
        
        left.inlineTableHandler(relation='@bunker_righe',viewResource='ViewFromBunkerRighe')
    
    @public_method
    def deleteImage(self, image=None, **kwargs):
        image_path = self.sitepath + re.sub('/_storage/site', '',image).split('?',1)[0]
        os.remove(image_path)
        self.setInClientData(value=None, path='shipsteps_arrival.form.shipsteps_bunker.form.record.stamp_transp')

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_cartella,stampa_bunker,email_bunker_transp,email_antifire,email_bunker,stampa_bunker_docs,*,10')
        btn_cartella_print=bar.stampa_cartella.button('Print Bunker folder')
        btn_bunker_print=bar.stampa_bunker.button('Print Bunker application')
        btn_bunker_emailtrasp=bar.email_bunker_transp.button('Email Bunker to Transportion')
        btn_email_antifire=bar.email_antifire.button('Email Antifire Service')
        btn_bunker_email=bar.email_bunker.button('Email Bunker application CP')
        btn_bunker_docs=bar.stampa_bunker_docs.button('Print docs after Bunker')
        btn_cartella_print.dataRpc('nome_temp', self.print_template_bunker,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.bunker:cartella_bunker',format_page='A3')
        btn_bunker_print.dataRpc('nome_temp', self.print_template_bunker,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.bunker:bunker',format_page='A4')
        #definiamo la tabella email_services per poi riprenderla sui dataRpc dei bottoni
        tbl_email_services = self.db.table('shipsteps.email_services')                            
        #verifichiamo quanti servizi CP ci sono, nel caso più di uno apparirà la dbSelect per la scelta
        service_for_email = tbl_email_services.query(columns="$service_for_email_id", where='$service_for_email_id=:serv', serv='cp').fetch()
        serv_len=len(service_for_email)
        if serv_len > 1:                                   
            btn_bunker_email.dataRpc('nome_temp', self.print_template_bunker,record='=#FORM.record',servizio=['capitaneria'], email_template_id='email_bunker_cp',
                                nome_template = 'shipsteps.bunker:bunker',format_page='A4',
                                _ask=dict(title='!![en]Select the services<br>Select the Attachments<br>Insert the safety data sheets and antifire request confirmation',fields=[dict(name='services', lbl='!![en]Services', tag='dbSelect',hasDownArrow=True,
                                table='shipsteps.email_services', columns='$consignee', auxColumns='$email,$email_cc,$email_bcc,$email_pec,$email_cc_pec',condition="$service_for_email_id=:cod",condition_cod='cp',alternatePkey='consignee',
                                validate_notnull=True,cols=4,popup=True,colspan=2, hasArrowDown=True),dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                                 table='shipsteps.bunker_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',width='22em',
                                 cols=4,popup=True,colspan=2),dict(name='type_atc',lbl='!![en]Type atc',tag='filteringSelect',values='zip:zip,unzip:non compresso')])) 
        else:
            btn_bunker_email.dataRpc('nome_temp', self.print_template_bunker,record='=#FORM.record',servizio=['capitaneria'], email_template_id='email_bunker_cp',
                                nome_template = 'shipsteps.bunker:bunker',format_page='A4',_ask=dict(title='!![en]Select the Attachments<br>Insert the safety data sheets and antifire request confirmation',fields=[dict(name='allegati', lbl='!![en]Attachments', tag='checkboxtext',
                                 table='shipsteps.bunker_atc', columns='$description',condition="$maintable_id =:cod",condition_cod='=#FORM.record.id',width='22em',
                                 cols=4,popup=True,colspan=2),dict(name='type_atc',lbl='!![en]Type atc',tag='filteringSelect',values='zip:zip,unzip:non compresso')]))
        btn_bunker_emailtrasp.dataRpc('nome_temp', self.print_template_bunker,record='=#FORM.record',servizio=['trasportatore'], email_template_id='email_bunker_transp',
                            nome_template = 'shipsteps.bunker:bunker_transp',format_page='A4')
        #verifichiamo quanti servizi Antifire ci sono, nel caso più di uno apparirà la dbSelect per la scelta
        service_for_email = tbl_email_services.query(columns="$service_for_email_id", where='$service_for_email_id=:serv', serv='antfire').fetch()
        serv_len=len(service_for_email)  
        if serv_len > 1:                  
            btn_email_antifire.dataRpc('nome_temp', self.print_template_bunker,record='=#FORM.record',servizio=['antifire'], email_template_id='email_antifire',
                                nome_template = 'shipsteps.bunker:bunker_antifire',format_page='A4',
                                _ask=dict(title='!![en]Select the services',fields=[dict(name='services', lbl='!![en]Services', tag='dbSelect',hasDownArrow=True,
                                    table='shipsteps.email_services', columns='$consignee', auxColumns='$email,$email_cc,$email_bcc,$email_pec,$email_cc_pec',condition="$service_for_email_id=:cod",condition_cod='antfire',alternatePkey='consignee',
                                    validate_notnull=True,cols=4,popup=True,colspan=2, hasArrowDown=True)]))  
        else:
            btn_email_antifire.dataRpc('nome_temp', self.print_template_bunker,record='=#FORM.record',servizio=['antifire'], email_template_id='email_antifire',
                                nome_template = 'shipsteps.bunker:bunker_antifire',format_page='A4')                                      
        btn_bunker_docs.dataRpc('nome_temp', self.print_template_bunker,record='=#FORM.record',servizio=[''], email_template_id='',
                            nome_template = 'shipsteps.bunker:bunker_docs',format_page='A4')                           
    
    @public_method
    def print_template_bunker(self, record, resultAttr=None, nome_template=None, email_template_id=None,servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        #print(x)
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special
        if email_template_id=='email_bunker_cp' and kwargs['allegati'] is not None:
            lista_all=list(kwargs['allegati'].split(","))
        else:
            lista_all=None    
        tbl_bulk = self.db.table('shipsteps.bunker')
        builder = TableTemplateToHtml(table=tbl_bulk)

        nome_temp = nome_template.replace('shipsteps.bunker:','')
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
        if email_template_id == 'email_bunker_cp':
            self.email_services(record,email_template_id,servizio,lista_all, **kwargs)
            nome_temp='val_bulk'
            return nome_temp
        if email_template_id == 'email_bunker_transp':
            self.email_trasportatore(record,email_template_id,servizio, **kwargs)
            nome_temp='val_bulk'
            return nome_temp
        if email_template_id == 'email_antifire':
            self.email_antifire(record,email_template_id,servizio, **kwargs)
        #se ritorna il valore di self.msg_pecial dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di self.ms_special alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
            nome_temp='val_bulk'
            return nome_temp

    @public_method
    def email_services(self, record,email_template_id=None,servizio=[],lista_all=None, **kwargs):
        id_bunker_atc=record['id']
        record=record['arrival_id']        
        if not record:
            return

        #leggiamo nei kwargs la tipologia dell'allegato se zip oppure non compresso
        type_atc = None
        for chiavi in kwargs.keys():    
            if chiavi=='type_atc':
                if kwargs['type_atc']:
                    type_atc=kwargs['type_atc']  

        #lettura degli attachment
        attcmt=[]
        attcmt_name=[]
        if lista_all is not None:
            len_allegati = len(lista_all) #verifichiamo la lunghezza della lista pkeys tabella allegati
            file_url=[]
            tbl_att =  self.db.table('shipsteps.bunker_atc') #definiamo la variabile della tabella allegati
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
                attcmt_name.append(Path(fileSn.internal_path).name)
       # tbl_att =  self.db.table('shipsteps.bunker_atc')
       # fileurl = tbl_att.query(columns='$fileurl',
       #           where='$maintable_id=:mt_id',mt_id=id_bunker_atc).fetch()
       # ln = len(fileurl)
       # attcmt=[]
       # attcmt_name=[]
       # 
       # for r in range(ln):
       #     file_url = fileurl[r][0]
       #     file_path = file_url.replace('/home','site')
       #     fileSn = self.site.storageNode(file_path)
       #     attcmt.append(fileSn.internal_path)
       #     attcmt_name.append(Path(fileSn.internal_path).name)
        
        #Condizioniamo l'aggiunta dell'allegato se il servizio invio email è per la cp
        if email_template_id=='email_bunker_cp':
            
            file_path = 'site:stampe_template/bunker.pdf'
            fileSn = self.site.storageNode(file_path)
            attcmt.append(fileSn.internal_path)
            attcmt_name.append(Path(fileSn.internal_path).name)

            pdfpath = self.site.storageNode('home:stampe_template')
            pdfpath=pdfpath.internal_path
            with zipfile.ZipFile(pdfpath + "/bunker.zip", mode="w") as archive:
               
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
        tbl_staff =  self.db.table('shipsteps.staff')
        account_email = tbl_staff.readColumns(columns='$email_account_id',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('shipsteps.agency')
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

    @public_method
    def email_trasportatore(self, record,email_template_id=None,servizio=[], **kwargs):
        record_id=record['arrival_id']
        if not record:
            return
        #lettura del record_id della tabella arrival
        
        #lettura dati su tabella arrival
        tbl_arrival = self.db.table('shipsteps.arrival')
        vessel_type,vessel_name,eta_arr,ref_numb = tbl_arrival.readColumns(columns='@vessel_details_id.@imbarcazione_id.tipo,@vessel_details_id.@imbarcazione_id.nome,$eta,$reference_num',
                  where='$agency_id=:ag_id AND $id=:rec_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'),rec_id=record_id)
        eta = eta_arr.strftime("%d/%m/%Y, %H:%M")    
        
        #creiamo la variabile lista attcmt dove tramite il ciclo for andremo a sostituire la parola 'site' con '/home'
        attcmt=[]
        
         #Condizioniamo l'aggiunta dell'allegato se il servizio invio email è il garbage
        if email_template_id=='email_bunker_transp':
            
            file_path = 'site:stampe_template/bunker_transp.pdf'
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
        #services=kwargs['services']
        #trasformiamo la stringa services in una lista
        #servizio=list(services.split(","))
        
        
        
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
       
        consignee='a: ' + record['ditta_trasp']
        subject='Istanza bunker '+vessel_type + ' ' + vessel_name + ' ref:' + ref_numb #record['ref_number']
        body_header="""<span style="font-family:courier new,courier,monospace;">""" + 'da: '+ agency_name + '<br>' + consignee + '<br><br>'
        body_footer= 'Cordiali saluti<br><br>' + user_fullname + '<br><br>' + ag_fullstyle + """</span></div>"""
        
        body_msg=(sal + '<br>' + "in allegato istanza bunker del/lla " +vessel_type + ' ' + vessel_name + " che Vi preghiamo di compilare in tutte le parti mancanti" + '<br>'
                    + "e rinviare assieme a:" + '<br><br>'+ "- Documento di riconoscimento dell'autista (fronte/retro) per l'accesso in porto" + '<br>' + "- Scheda di sicurezza prodotto" + '<br>'
                      "- Scheda tecnica del prodotto" + '<br><br>')
        body_html=(body_header + body_msg + body_footer )
        #print(x)
        email_to=record['email_transp']
        if (email_to) is not None:
            self.db.table('email.message').newMessage(account_id=account_email,
                           to_address=email_to,
                           from_address=email_mittente,
                           subject=subject, body=body_html, 
                           attachments=attcmt,
                           html=True)
            self.db.commit()
        
        if email_to is not None:
            nome_temp='val_upd'
            return nome_temp
        
    @public_method
    def email_antifire(self, record,email_template_id=None,servizio=[], **kwargs):
        record=record['id']
        if not record:
            return

        #creiamo la variabile lista attcmt dove tramite il ciclo for andremo a sostituire la parola 'site' con '/home'
        attcmt=[]
        
         #Condizioniamo l'aggiunta dell'allegato se il servizio invio email è il garbage
        if email_template_id=='email_antifire':
            
            file_path = 'site:stampe_template/bunker_antifire.pdf'
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
                                                          table='shipsteps.bunker',
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
                                                          table='shipsteps.bunker',
                                                          account_id = account_emailpec,
                                                          to_address=email_pec,
                                                          cc_address=email_pec_cc,
                                                          attachments=attcmt,
                                                          template_code=email_template_id)
            self.db.commit()
        
        
        if (email_dest or email_pec_dest) is not None:

          # if servizio == ['capitaneria']:
            
            return