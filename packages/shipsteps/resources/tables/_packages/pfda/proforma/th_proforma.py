#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrnumber import decimalRound
from gnr.core.gnrbag import Bag
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
from gnr.core.gnrlang import GnrException

class ViewProforma(BaseComponent):

    def th_options(self):
        return dict(partitioned=True)

class Form(BaseComponent):

    def th_bottom_custom(self, bottom):
        if self.db.currentEnv.get('current_agency_id'):

            bar = bottom.slotBar('10,stampa_proforma,5,crea_email,*,10')
            btn_proforma=bar.stampa_proforma.button('Print Proforma')
            btn_proforma.dataRpc('nome_temp', self.print_template,record='=#FORM.record', email_template_id=None,
                            nome_template = 'pfda.proforma:proforma',format_page='A4')
            #prendiamo l'account email con cui inviamo le email da Staff
            tbl_staff=self.db.table('shipsteps.staff')
            email_account_id = tbl_staff.readColumns(columns='$email_account_id',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
            #email_account_id = self.db.application.getPreference('mail.account_id',pkg='pfda')
            email_template_id = self.db.application.getPreference('tpl.template_id',pkg='pfda')
            btn_creaemail=bar.crea_email.button('Crea email proforma')
            btn_creaemail.dataRpc('msg_special', self.print_template, record='=#FORM.record',
                                  email_template_id=email_template_id,nome_template = 'pfda.proforma:proforma',
                                  email_account_id=email_account_id)
            bar.dataController("""if(msgspec=='proforma') genro.publish("floating_message",{message:msg_txt, messageType:"message"});""",msgspec='^msg_special', msg_txt = 'Email ready to be sent')

    @public_method
    def print_template(self, record, resultAttr=None, nome_template=None, email_template_id=None, format_page=None,email_account_id=None, **kwargs):
        record_arr=record['id']
        # Crea stampa
        tbl_proforma = self.db.table('pfda.proforma')
        builder = TableTemplateToHtml(table=tbl_proforma)
        #nome_template = nome_template #'shipsteps.arrival:check_list'
        prot_proforma = record['protocollo']
        prot_proforma = prot_proforma.replace("/", "")
        nome_file = str.lower('{cl_id}.pdf'.format(
                    cl_id=prot_proforma[0:]))#record[0:])

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:proforma', nome_file)

        tbl_agency = self.db.table('shipsteps.agency')
        #tbl_template=self.db.table('adm.htmltemplate')
        letterhead = tbl_agency.readColumns(columns='$htmltemplate_id',
                  where='$id=:ag_id', ag_id=self.db.currentEnv.get('current_agency_id'))
        # (pdfpath.internal_path)
        #print(x)
       #if kwargs:
       #    letterhead=kwargs['letterhead_id']
       #else:
       #    letterhead=''

        builder(record=record_arr, template=template,letterhead_id=letterhead)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290

        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                             value=result.url(timestamp=datetime.now()), fired=True)
        if email_template_id is not None:

            self.invia_proforma(record,email_account_id,email_template_id, **kwargs)
            msg_special='proforma'
            return msg_special

    @public_method
    def invia_proforma(self, record,email_account_id,email_template_id, **kwargs):
        tbl_proforma = self.db.table('pfda.proforma')
        if not record:
            return

        record_id=record['id']
        nome_file=record['pathtopdf']
        pdfpath = self.site.storageNode('home:proforma', nome_file)
        attcmt = [pdfpath.internal_path]

        #verifichiamo il secondo allegato info port nella tabella fileforemail
        tbl_file =  self.db.table('pfda.fileforemail') #definiamo la variabile della tabella allegati
        att = tbl_file.query(columns="$pathfile", where='').fetch()
        len_att=len(att)
        for r in range(len_att):
            url_allegato=att[r][0]
            #url_att = url_allegato.replace('home:','site/')#cambiamo al url_allegato la posizione home: in site/
            #print(x)
            attcmt.append(url_allegato)#appendiamo agli attcmt l'url_allegato aggiungendoci il path iniziale

        self.db.table('email.message').newMessageFromUserTemplate(
                                                      record_id=record_id,
                                                      table='pfda.proforma',
                                                      attachments=attcmt,
                                                      account_id = email_account_id,
                                                      template_id=email_template_id)

        self.db.commit()

        return
