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
        r.fieldcell('port')
        r.fieldcell('vessel_details_id', width='30em')
        r.fieldcell('email_to')
        r.fieldcell('email_cc')
        r.fieldcell('prearr_descr')
        r.fieldcell('__ins_ts')
        r.fieldcell('data_invio')

    def th_order(self):
        return '__ins_ts:d'

    def th_query(self):
        return dict(column='port', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px', fld_width='30em')
        fb.field('port', colspan=2)
        fb.field('vessel_details_id', colspan=2, hasDownArrow=True)
        fb.div("!![en]Insert the emails separate by commas",font_weight='bold', margin_top='10px')
        fb.br()
        fb.field('email_to', colspan=2,tag='textarea', height='5em')
        fb.div("!![en]Insert the emails separate by commas",font_weight='bold', margin_top='10px')
        fb.br()
        fb.field('email_cc',colspan=2,tag='textarea', height='5em')
        fb.field('prearr_descr',tag='dbSelect', hasDownArrow=True, colspan=2)
        fb.field('data_invio', readOnly=True, disabled=True)

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,email_prearr,*,10')
        btn_email_prearr=bar.email_prearr.button('!![en]Email Pre-Arrivals')
        btn_email_prearr.dataRpc('nome_temp', self.email_prearrival,record='=#FORM.record', email_template_id='prearrivals',
                                    _ask=dict(title='!![en]Select if you want a zipped file',
                                    fields=[dict(name='type_atc',lbl='!![en]Type atc',tag='filteringSelect',values='zip:zip,unzip:non compresso')]),
                                    _onResult="this.form.save();this.form.reload();")
        bar.dataController("""if(msgspec=='prearrivals') {genro.publish("floating_message",{message:msg_txt, messageType:"message"});}""",
                            msgspec='^nome_temp', msg_txt = 'Email ready to be sent')
                           

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

    @public_method
    def email_prearrival(self, record,email_template_id=None, **kwargs):
        #print(x)
        id_prearr_atc=record['prearr_descr']
        record_id=record['id']        
        if not record_id:
            return
        #leggiamo nei kwargs la tipologia dell'allegato se zip oppure non compresso
        type_atc = None
        for chiavi in kwargs.keys():    
            if chiavi=='type_atc':
                if kwargs['type_atc']:
                    type_atc=kwargs['type_atc']   

        tbl_att =  self.db.table('shipsteps.prearrivals_default_atc')
        fileurl = tbl_att.query(columns='$fileurl',
                  where='$maintable_id=:mt_id',mt_id=id_prearr_atc).fetch()
        ln = len(fileurl)
        attcmt=[]
        attcmt_name=[]
        
        for r in range(ln):
            file_url = fileurl[r][0]
            file_path = file_url.replace('/home','site')
            fileSn = self.site.storageNode(file_path)
            attcmt.append(fileSn.internal_path)
            attcmt_name.append(Path(fileSn.internal_path).name)
        
        if email_template_id=='prearrivals':

            pdfpath = self.site.storageNode('home:shipsteps_prearrivals_default')
            pdfpath=pdfpath.internal_path
            with zipfile.ZipFile(pdfpath + "/prearrivals.zip", mode="w") as archive:
               
                for filenamedir,filename in zip(attcmt,attcmt_name):
                     archive.write(filenamedir,filename)
        
        if type_atc == 'zip':
            attcmt=archive.filename
        elif type_atc == 'unzip':
            attcmt
        else:
            attcmt  
        
        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('shipsteps.staff')
        account_email = tbl_staff.readColumns(columns='$email_account_id',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('shipsteps.agency')
        account_emailpec = tbl_agency.readColumns(columns='$emailpec_account_id',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))                
        
        email_to = record['email_to']
        email_cc = record['email_cc']
        email_bcc = ''
        
        if (email_to) is not None:
            self.db.table('email.message').newMessageFromUserTemplate(
                                                          record_id=record_id,
                                                          table='shipsteps.prearrivals',
                                                          account_id = account_email,
                                                          to_address=email_to,
                                                          cc_address=email_cc,
                                                          bcc_address=email_bcc,
                                                          attachments=attcmt,
                                                          template_code=email_template_id)
            self.db.commit()
        
        
        if (email_to) is not None:
            #avendo preso il valore services nei kwargs ossia il consignee dell'email sevices andiamo a copiarlo nel record della tasklist nome_servizio 
            data_corrente = datetime.now()
            tbl_prearrivals = self.db.table('shipsteps.prearrivals')  
            tbl_prearrivals.batchUpdate(dict(data_invio=data_corrente),
                                        where='$id=:id_prearr', id_prearr=record_id)
            self.db.commit()
        
          # if servizio == ['capitaneria']:
            nome_temp = 'prearrivals'
            return nome_temp