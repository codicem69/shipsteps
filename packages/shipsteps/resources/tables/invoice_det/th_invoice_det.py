#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
       
        r.fieldcell('rag_sociale', width='30em')
        r.fieldcell('address', width='30em')
        r.fieldcell('cap', width='7em')
        r.fieldcell('city')
        r.fieldcell('vat')
        r.fieldcell('cf')
        r.fieldcell('cod_univoco')
        r.fieldcell('pec', width='15em')

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='rag_sociale', op='contains', val='')

class ViewIntFat(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()  
        r.fieldcell('fullname',width='100%')
    
    def th_view(self,view):
        bar = view.top.slotToolbar('*,intfat,5')
        btn_email_intfat=bar.intfat.button('Email Intestazione fattura')
        btn_email_intfat.dataRpc('nome_temp', self.email_intfat,record='=#FORM.record',nome_vs='=#FORM.record.@vessel_details_id.@imbarcazione_id.nome')

    @public_method
    def email_intfat(self, record, **kwargs):
        ref_num=record['reference_num']
        arrival_id=record['id']
        if not record:
            return
        #lettura del record_id della tabella arrival
        record_id=record['id']
        vessel_type = record['@vessel_details_id.@imbarcazione_id.tipo']
        vessel_name = record['@vessel_details_id.@imbarcazione_id.nome']
        intfat_id = record['invoice_det_id']
        tbl_invoice = self.db.table('shipsteps.invoice_det')
        int_fat = tbl_invoice.readColumns(columns="""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'') || coalesce(' - Vat: ' || $vat,'') || 
                                     coalesce(' - unique code: ' || $cod_univoco,'') || coalesce(' - pec: ' || $pec,'') AS rag_soc""", where='$id=:id_inv',id_inv=intfat_id)
        #rag_soc,indirizzo,cap,citta,vat,cf,cod_un,pec = tbl_invoice.readColumns(columns='$rag_sociale,$address,$cap,$city,$vat,$cf,$cod_univoco,$pec', where='$id=:id_inv',id_inv=intfat_id)
        if int_fat == [None, None, None, None, None, None, None]:
            nome_temp='no_int'
            return nome_temp
        
        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('agz.staff')
        account_email,email_mittente,user_fullname = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,$fullname',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        tbl_agency =  self.db.table('agz.agency')
        agency_name,ag_fullstyle,account_emailpec,emailpec_mitt = tbl_agency.readColumns(columns='$agency_name,$fullstyle,$emailpec_account_id, @emailpec_account_id.address',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        
        
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
       
        subject='Intestazione fatture '+vessel_type + ' ' + vessel_name + ' ref:' + record['reference_num']
        #body_header="""<span style="font-family:courier new,courier,monospace;">""" + 'da: '+ agency_name + '<br>' + consignee + '<br><br>'
        body_footer= 'Cordiali saluti<br><br>' + user_fullname + '<br><br>' + ag_fullstyle + """</span></div>"""
        
        body_msg=("""<span style="font-family:courier new,courier,monospace;">""" + sal + '<br>' + "con la presente siamo a girarVi intestazione fatture per " +vessel_type + ' ' + vessel_name + " :" + '<br><br>' +
                        int_fat + '<br><br>')
        body_html=(body_msg + body_footer )
        #print(x)
        
        self.db.table('email.message').newMessage(account_id=account_email,
                           to_address='',
                           from_address=email_mittente,
                           subject=subject, body=body_html, 
                           cc_address='',ref_num=ref_num,
                           arrival_id=arrival_id,html=True)
        self.db.commit()
        
        nome_temp='intfat'
        return nome_temp
        
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        
        fb.field('rag_sociale', width='54em',colspan=2 )
        fb.br()
        fb.field('address', width='30em' )
        fb.field('cap' )
        fb.field('city', width='30em' )
        fb.field('vat' )
        fb.field('cf' )
        fb.field('cod_univoco' )
        fb.field('pec' )


    def th_options(self):
        return dict(dialog_windowRatio = 1 , annotations= True )
        #return dict(dialog_height='600px', dialog_width='800px' )
