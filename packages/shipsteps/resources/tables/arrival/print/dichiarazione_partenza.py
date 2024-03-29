from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.core.gnrstring import slugify
from datetime import datetime
import string
from gnr.core.gnrdecorator import public_method
import os
#from gnr.core.gnrlang import GnrException

caption = 'Dich.integrativa Partenza CP'

class Main(BaseResourcePrint):
    batch_title = 'Dich.integrativa Partenza CP'
    html_res = 'html_res/nota_partenza_cp'
    batch_immediate = 'print'
    batch_thermo_lines = 'batch_steps,batch_main,ts_loop'
    virtual_columns = "@agency_id.fullstyle"
    py_requires = """gnrcomponents/drop_uploader"""
    def table_script_parameters_pane(self, pane, **kwargs):

        fb = pane.formbuilder(cols=2,border_spacing='3px')

        fb.textbox(value='^.car_deck', lbl='!![en]Cargo on deck',default='NIL',validate_notnull=True, colspan=2,width='36em')
        #fb.textbox(value='^.pax_imb', lbl='!![en]Passengers embarked',default='0',validate_notnull=True)
        fb.textbox(value='^.hazmat', lbl='HAZMAT',default='NIL',validate_notnull=True)
        fb.dateTextBox(value='^.data_att', lbl='Data doc.',default=self.db.workdate, validate_notnull=True)
        fb.br()
        fb.div('Timbro Nave')
        fb.br()
        fb.textbox(value='^.vess_stamp', validate_notnull=True, hidden=True)
        fb.div(border='2px dotted silver', width='150px', height='150px').img(
                    src='^.vess_stamp',
                    crop_width='150px',
                    crop_height='150px',
                    edit=True,
                    placeholder=True,
                    upload_filename='timbro_nave',
                    upload_folder='site:image')

    def result_handler_pdf(self, resultAttr):

        if not self.results:
            return '{btc_name} completed'.format(btc_name=self.batch_title), dict()
        save_as = slugify(self.print_options.get('save_as') or self.batch_parameters.get('save_as') or '')

        if not save_as:
            if len(self.results)>1:
                save_as = 'multiple_dich_integr_partenza' #slugify(self.batch_title)
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
