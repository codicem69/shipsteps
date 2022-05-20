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
        fb = center.formbuilder(cols=3, border_spacing='4px')
        #fb.field('arrival_id')
        fb.field('datetime_bunk')
        fb.field('rank_off')
        fb.field('name_off')
        fb.field('service')
        fb.field('durata')
        fb.br()
        fb.field('ditta_trasp')
        fb.field('iscr_dt')
        fb.field('lg_ditta_transp')
        fb.field('ditta_forn')
        fb.field('iscr_forn')
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
        bar = bottom.slotBar('10,stampa_cartella,stampa_bunker,email_bunker,*,10')
        btn_cartella_print=bar.stampa_cartella.button('Print Bunker folder')
        btn_bunker_print=bar.stampa_bunker.button('Print Bunker application')
        btn_bunker_email=bar.email_bunker.button('Email Bunker application CP')
        btn_cartella_print.dataRpc('msg_special', self.print_template_bunker,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.bunker:cartella_bunker',format_page='A3')
        btn_bunker_print.dataRpc('msg_special', self.print_template_bunker,record='=#FORM.record',servizio=[], email_template_id='',
                            nome_template = 'shipsteps.bunker:bunker',format_page='A4')
        btn_bunker_email.dataRpc('msg_special', self.print_template_bunker,record='=#FORM.record',servizio=['capitaneria'], email_template_id='email_bunker_cp',
                            nome_template = 'shipsteps.bunker:bunker',format_page='A4')
    
    @public_method
    def print_template_bunker(self, record, resultAttr=None, nome_template=None, email_template_id=None,servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        #print(x)
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special
        
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
        if email_template_id != '':
            self.email_services(record,email_template_id,servizio)
       
        #se ritorna il valore di self.msg_pecial dalla funzione sopra lanciata self.email_services
        # facciamo ritornare il valore di self.ms_special alla chiamata iniziale del bottone di stampa per far scattare
        # il msg con il dataController
            msg_special='val_bulk'
            return msg_special

    @public_method
    def email_services(self, record,email_template_id=None,servizio=[], **kwargs):
        id_rinfusa_atc=record['id']
        record=record['arrival_id']        
        if not record:
            return
        tbl_att =  self.db.table('shipsteps.bunker_atc')
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