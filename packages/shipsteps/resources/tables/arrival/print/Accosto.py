from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.core.gnrstring import slugify
from datetime import datetime
import string
from gnr.core.gnrdecorator import public_method
#from gnr.core.gnrlang import GnrException

caption = 'Domanda Accosto'

class Main(BaseResourcePrint):
    batch_title = 'Domanda Accosto'
    html_res = 'html_res/domanda_accosto'
    batch_immediate = 'print'
    virtual_columns = "@agency_id.fullstyle"

    def table_script_parameters_pane(self, pane, **kwargs):
        fb = pane.formbuilder(cols=1,border_spacing='3px')
        fb.div("--- Select the Consignee ---")
        fb.dbselect(value='^.email_dest', table='shipsteps.email_services', lbl='Email service', selected_consignee='.consignee',hasDownArrow=True
                    ,condition="$service_for_email_id=:cod",condition_cod='cp',validate_notnull=True)

    def result_handler_pdf(self, resultAttr, **kwargs):
        if not self.results:
            return '{btc_name} completed'.format(btc_name=self.batch_title), dict()
        save_as = slugify(self.print_options.get('save_as') or self.batch_parameters.get('save_as') or '')

        if not save_as:
            if len(self.results)>1:
                save_as = 'multiple_domanda_accosto' #slugify(self.batch_title)
            else:
                save_as =  self.page.site.storageNode(self.results['#0']).cleanbasename[:]


        outputFileNode=self.page.site.storageNode('home:stampe_template', save_as,autocreate=-1)

        #outputFileNode=self.page.site.storageNode('/home/tommaso/Documenti/Agenzia/PROFORMA', save_as,autocreate=-1)
        #self.print_options.setItem('zipped', True) # settando il valore zipped a True ottengo un file zippato
        zipped =  self.print_options.get('zipped')
        immediate_mode = self.batch_immediate
        if immediate_mode is True:
            immediate_mode = self.batch_parameters.get('immediate_mode')
        if immediate_mode and zipped:
            immediate_mode = 'download'
        if zipped:
            outputFileNode.path +='.zip'
            self.page.site.zipFiles(list(self.results.values()), outputFileNode)
        else:
            outputFileNode.path +='.pdf'
            self.pdf_handler.joinPdf(list(self.results.values()), outputFileNode)
        self.fileurl = outputFileNode.url(nocache=True, download=True)
        inlineurl = outputFileNode.url(nocache=True)
        resultAttr['url'] = self.fileurl
        resultAttr['document_name'] = save_as
        resultAttr['url_print'] = 'javascript:genro.openWindow("%s","%s");' %(inlineurl,save_as)
        if immediate_mode:
            resultAttr['autoDestroy'] = 600
        if immediate_mode=='print':
            self.page.setInClientData(path='gnr.clientprint',value=inlineurl,fired=True)
        elif immediate_mode=='download':
            self.page.setInClientData(path='gnr.downloadurl',value=inlineurl,fired=True)

        if outputFileNode:

            path_pdf = outputFileNode.internal_path

        #dal path_pdf del file in stampa verifichiamo la posizione di site in modo che quando preleviamo l'url degli attachments
        #possiamo aggiungere il path iniziale
        pos_site=str.find(path_pdf,"site")

        #prendiamo i record degli attachments vessel details
        vd_id=self.get_selection(columns='vessel_details_id, agency_id').output('list')[0][0]

        attcmt=[]
        file_url=[]
        #aggiungiamo agli attachments il file che andiamo a stampare
        attcmt.append(path_pdf)
        #leggiamo gli allegati della nave e li inseriamo negli attachments
        tbl_att =  self.db.table('shipsteps.vessel_details_atc') #definiamo la variabile della tabella allegati
        att = tbl_att.query(columns="$filepath", where='$maintable_id=:m_id and $att_email=True',
                                                                    m_id=vd_id).fetch()
        len_att=len(att)
        for r in range(len_att):
            url_allegato=att[r][0]
            url_att = url_allegato.replace('home:','site/')#cambiamo al url_allegato la posizione home: in site/
            attcmt.append(path_pdf[0:pos_site]+url_att)#appendiamo agli attcmt l'url_allegato aggiungendoci il path iniziale

        #leggiamo gli allegati dell'arrivo e li inseriamo negli attachments
        arr_id=self._pkeys[0]
        tbl_att =  self.db.table('shipsteps.arrival_atc') #definiamo la variabile della tabella allegati
        att = tbl_att.query(columns="$filepath", where='$maintable_id=:a_id and $att_email=True',
                                                                    a_id=arr_id).fetch()
        len_att=len(att)
        for r in range(len_att):
            url_allegato=att[r][0]
            url_att = url_allegato.replace('home:','site/')
            attcmt.append(path_pdf[0:pos_site]+url_att)

        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('agz.staff')
        account_email,email_mittente,user_fullname = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,$fullname',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

        tbl_agency =  self.db.table('agz.agency')
        agency_name,ag_fullstyle,account_emailpec,emailpec_mitt = tbl_agency.readColumns(columns='$agency_name,$fullstyle,$emailpec_account_id, @emailpec_account_id.address',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

        #Lettura degli indirizzi email destinatari
        email_dest_id=self.batch_parameters['email_dest']
        #servizio=['cpnsw']
        #ln_serv=len(servizio)

        #assegnamo le varibili liste per inserire successivamente i risultati della ricerca sulla tabella email_services
        destinatario,destinatario_pec,email_d, email_cc_d,email_bcc_d, email_pec_d, email_pec_cc_d=[],[],[],[],[],[],[]
        #definiamo la variabile contentente la tabella email_services
        tbl_email_services=self.db.table('shipsteps.email_services')
        #con il ciclo for ad ogni passaggio otteniamo il nome del servizio che passeremo alla query e i risultati saranno appesi alle liste
        #for serv in servizio:
        #    dest,email_dest, email_cc_dest,email_bcc_dest = tbl_email_services.readColumns(columns="""$consignee,$email,$email_cc,$email_bcc""",
        #                                            where="$service_for_email_id=:serv AND $agency_id=:ag_id", serv=serv,
        #                                            ag_id=self.db.currentEnv.get('current_agency_id'))
        #    dest_pec,email_pec_dest, email_pec_cc_dest = tbl_email_services.readColumns(columns="""$consignee,$email_pec,$email_cc_pec""",
        #                                            where='$service_for_email_id=:serv AND $agency_id=:ag_id AND $email_pec IS NOT NULL', serv=serv,
        #                                            ag_id=self.db.currentEnv.get('current_agency_id'))
        #    if dest is not None and dest !='':
        #        destinatario.append('a: ' + dest)
        #    if dest_pec is not None and dest_pec !='':
        #        destinatario_pec.append('a: ' + dest_pec)
        #    if email_dest is not None and email_dest !='':
        #        email_d.append(email_dest)
        #    if email_cc_dest is not None and email_cc_dest != '':
        #        email_cc_d.append(email_cc_dest)
        #    if email_bcc_dest is not None and email_bcc_dest != '':
        #        email_bcc_d.append(email_bcc_dest)
        #    if email_pec_dest is not None and email_pec_dest != '':
        #        email_pec_d.append(email_pec_dest)
        #    if email_pec_cc_dest is not None and email_pec_cc_dest !='':
        #        email_pec_cc_d.append(email_pec_cc_dest)
        dest,email_dest, email_cc_dest,email_bcc_dest = tbl_email_services.readColumns(columns="""$consignee,$email,$email_cc,$email_bcc""",
                                                    where="$id=:ed_id AND $agency_id=:ag_id", ed_id=email_dest_id,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'))
        dest_pec,email_pec_dest, email_pec_cc_dest = tbl_email_services.readColumns(columns="""$consignee,$email_pec,$email_cc_pec""",
                                                    where='$id=:ed_id AND $agency_id=:ag_id AND $email_pec IS NOT NULL', ed_id=email_dest_id,
                                                    ag_id=self.db.currentEnv.get('current_agency_id'))
        if dest is not None and dest !='':
            destinatario.append('a: ' + dest)
        if dest_pec is not None and dest_pec !='':
            destinatario_pec.append('a: ' + dest_pec)
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
        consignee='<br>'.join([str(item) for item in destinatario])
        consignee_pec='<br>'.join([str(item) for item in destinatario_pec])
        email_to = ','.join([str(item) for item in email_d])
        email_cc = ','.join([str(item) for item in email_cc_d])
        email_bcc = ','.join([str(item) for item in email_bcc_d])
        email_pec = ','.join([str(item) for item in email_pec_d])
        email_pec_cc = ','.join([str(item) for item in email_pec_cc_d])

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

        vessel_type = self.get_selection(columns='@vessel_details_id.@imbarcazione_id.tipo').output('list')[0][0]
        vessel_name = self.get_selection(columns='@vessel_details_id.@imbarcazione_id.nome').output('list')[0][0]
        visit_id =self.get_selection(columns='visit_id').output('list')[0][0]
        ref_n = self.get_selection(columns='reference_num').output('list')[0][0]

        subject='VISIT-ID:'+str(visit_id) + ' - Domanda Accosto ' + str(vessel_type) + ' ' + str(vessel_name) + ' ref:' + str(ref_n)
        body_header="""<span style="font-family:courier new,courier,monospace;">""" + 'da: '+ str(agency_name) + '<br>' + str(consignee) + '<br><br>'
        body_header_pec="""<span style="font-family:courier new,courier,monospace;">""" + 'da: '+ str(agency_name) + '<br>' + str(consignee_pec) + '<br><br>'
        body_footer= 'Cordiali saluti<br><br>' + str(user_fullname) + '<br><br>' + str(ag_fullstyle) + """</span></div>"""

        body_msg=(sal + '<br><br>' + "si allega domanda di accosto " +str(vessel_type) + ' ' + str(vessel_name) + '<br><br>')
        body_html=(body_header + body_msg + body_footer )

        if email_to:
            self.db.table('email.message').newMessage(account_id=account_email,
                           to_address=email_to,
                           from_address=email_mittente,
                           subject=subject, body=body_html,
                           cc_address=email_cc,
                           bcc_address=email_bcc, attachments=attcmt,
                           html=True)
            self.db.commit()

        body_html_pec=(body_header_pec + body_msg + body_footer )
        if email_pec is not None and email_pec!='':

            self.db.table('email.message').newMessage(account_id=account_emailpec,
                           to_address=email_pec,
                           from_address=emailpec_mitt,
                           subject=subject, body=body_html_pec,
                           cc_address=email_pec_cc,
                           attachments=attcmt,
                           html=True)
            self.db.commit()






