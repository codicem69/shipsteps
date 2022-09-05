from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.core.gnrstring import slugify


caption = 'General declaration arrival'

class Main(BaseResourcePrint):
    batch_title = 'General declaration arrival'
    html_res = 'html_res/general_declaration'
    batch_immediate = 'print'
    pdf_service = 'wk'

    def table_script_parameters_pane(self, pane, **kwargs):

        fb = pane.formbuilder(cols=2,border_spacing='3px')

        #fb.textbox(value='^.motivo_approdo', lbl='Motivo approdo',validate_notnull=True, colspan=2, width='40em')
        fb.textbox(value='^.cargo_decl', lbl='Cargo declaration',default='1',validate_notnull=True)
        fb.textbox(value='^.store_list', lbl='Store list',default='1',validate_notnull=True)
        fb.textbox(value='^.crew_list', lbl='Crew list',default='1',validate_notnull=True)
        fb.textbox(value='^.pax_list', lbl='Pax list',default='1',validate_notnull=True)
        fb.textbox(value='^.crew_effects', lbl='Crew effects',default='1',validate_notnull=True)
        fb.textbox(value='^.healt_decl', lbl='Healt declaration',default='1',validate_notnull=True)
        fb.dateTextBox(value='^.data_att', lbl='Data doc.',default=self.db.workdate, validate_notnull=True)

        fb.dataController("""if(msg=='sbarco')genro.publish("floating_message",{message:msg_txt, messageType:"message"});if(msg=='imbarco')genro.publish("floating_message",{message:"Error", messageType:"error"});""", msg='^.motivo_approdo',msg_txt = 'Email ready to be sent')
        #fb.dataController("if(msg=='sbarco') {alert('Message created')}", msg='^.motivo_approdo')

    def result_handler_pdf(self, resultAttr):

        if not self.results:
            return '{btc_name} completed'.format(btc_name=self.batch_title), dict()
        save_as = slugify(self.print_options.get('save_as') or self.batch_parameters.get('save_as') or '')

        if not save_as:
            if len(self.results)>1:
                save_as = 'multiple_general_decl' #slugify(self.batch_title)
            else:
                save_as =  self.page.site.storageNode(self.results['#0']).cleanbasename[:]


        outputFileNode=self.page.site.storageNode('home:stampe_template', save_as,autocreate=-1)
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
        #record = self.get_selection(columns='id').output('list')[0][0]
        #vessel_name = self.get_selection(columns='@vessel_details_id.@imbarcazione_id.nome').output('list')[0][0]
    
  # def onRecordPrinted(self,record,filepath):
  #     vessel_name=record['@vessel_details_id.@imbarcazione_id.nome']
  #     record=record['id']
  #     nome_file = 'Fal1_arr_' + vessel_name
  #     #pdfpath = self.page.site.storageNode('home:stampe_template', nome_file)
  #     tbl_arrival_atc = self.db.table('shipsteps.arrival_atc')
  #     if not tbl_arrival_atc.checkDuplicate(maintable_id=record,description=nome_file):
  #         tbl_arrival_atc.addAttachment(maintable_id=record,
  #                                       origin_filepath=filepath,
  #                                       description=nome_file,
  #                                       moveFile=True)
  #     self.db.commit()
