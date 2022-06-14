#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('shorepass_id')
        r.fieldcell('name')
        r.fieldcell('surname')
        r.fieldcell('rank')
        r.fieldcell('nationality')
        r.fieldcell('birth_date')
        r.fieldcell('birth_place')
        r.fieldcell('birth_country')
        r.fieldcell('gender')
        r.fieldcell('id_doc')
        r.fieldcell('id_doc_n')
        r.fieldcell('id_doc_state')
        r.fieldcell('expire_id_doc')
        r.fieldcell('expire')
        r.fieldcell('start_time')
        r.fieldcell('stop_time')
        r.fieldcell('shorepass')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')
   
class ViewFromShorepassRighe(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('shorepass_id', edit=True)
        r.fieldcell('name', edit=True)
        r.fieldcell('surname', edit=True)
        r.fieldcell('rank', edit=True)
        r.fieldcell('nationality', edit=True)
        r.fieldcell('birth_date', edit=True, width='7em')
        r.fieldcell('birth_place', edit=True, width='7em')
        r.fieldcell('birth_country', edit=True)
        r.fieldcell('gender', edit=True, width='7em')
        r.fieldcell('id_doc', edit=True)
        r.fieldcell('id_doc_n', edit=True)
        r.fieldcell('id_doc_state', edit=True)
        r.fieldcell('expire_id_doc', edit=True, width='7em')
        r.fieldcell('expire', edit=True,batch_assign=True, width='7em')
        r.fieldcell('start_time', edit=True,batch_assign=True, width='5em')
        r.fieldcell('stop_time', edit=True,batch_assign=True, width='5em')
        r.fieldcell('shorepass', edit=True)
    
    def th_order(self):
        return '_row_count'
   
    def th_view(self,view):
        bar = view.top.bar.replaceSlots('addrow','addrow,resourcePrints,10,importa_crew,10,batchAssign,10,stampa_shorepass')
        btn_importa_crew = bar.importa_crew.paletteImporter(paletteCode='xls_importer',
                            dockButton_iconClass=False,
                            title='!!Importa crew',
                            importButton_label='Importa crew',
                            previewLimit=50,
                            dropMessage='Trascina qui il tuo file o clicca per cercarlo', filetype='excel',
                            importButton_action="genro.publish('import_clienti',{filepath:imported_file_path})",
                            matchColumns='*')
        btn_print_shorepass=bar.stampa_shorepass.button('Stampa Shorepass')
        bar.dataRpc(self.importaCrew, subscribe_import_clienti=True,record='=#FORM.record',
                      _onResult="genro.publish('xls_importer_onResult',result);",
                      _onError="genro.publish('xls_importer_onResult',{error:error});")
        btn_print_shorepass.dataRpc('msg_special', self.print_template_shorepass,record='=#FORM.record',pkeys='=#FORM.shipsteps_shorepass_righe.view.grid.currentSelectedPkeys',servizio=[],
                            nome_template = 'shipsteps.shorepass_righe:shorepass_righe',format_page='A4')
    def th_order(self):
        return '_row_count'

   #def th_bottom_custom(self, bottom):
   #    bar = bottom.slotBar('10,importa_crew,*,10')
   #    btn_importa_crew=bar.importa_crew.paletteImporter(paletteCode='xls_importer',
   #                            dockButton_iconClass=False, 
   #                            title='!!Importa crew',
   #                            importButton_label='Importa crew',
   #                            previewLimit=50, 
   #                            dropMessage='Trascina qui il tuo file o clicca per cercarlo', 
   #                            filetype='excel', 
   #                            matchColumns='*', 
   #                            table='shipsteps.shorepass_righe',
   #                            importerMethod='con_nazioni')
    

    
    @public_method
    def importaCrew(self, filepath=None, record=None, **kwargs):
        "Importa Excel clienti con comuni"
        paesi =    self.db.table('unlocode.nazione').query(columns='$nome,$code').fetchAsDict('code')        
        reader = self.utils.getReader(filepath)
        result = Bag()
        shorepassid = record['id']

        for row in reader():
            if row['nationality']: 
                paese_id = paesi.get(row['nationality']).get('code') 
            else: 
                paese_id = None 
            if row['birth_country']:
                birthcountry = paesi.get(row['birth_country']).get('code')
            else:
                birthcountry = None
            if row['doc_state']:
                stateid = paesi.get(row['doc_state']).get('code')
            else:
                stateid = None

            new_crew = self.db.table('shipsteps.shorepass_righe').newrecord(shorepass_id=shorepassid,nome=row['name'],cognome=row['surname'],grado=row['rank'],nazionalita=paese_id,
                        data_nascita=row['birth_date'],luogo_nascita=row['birth_place'],paese_nascita=birthcountry,
                        sesso=row['gender'],id_doc=row['identity_doc'],id_doc_n=row['doc_n'],id_doc_state=stateid,
                        expire_id_doc=row['expire_doc'], **row)

            self.db.table('shipsteps.shorepass_righe').insert(new_crew)
            result.addItem('inserted_row', row)

        self.db.commit()
        return result

    @public_method
    def print_template_shorepass(self, record,pkeys=None, resultAttr=None, nome_template=None, servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        #pkey = ','.join([str(item) for item in pkeys])
        record_id=pkeys
        
        tbl_shorepass_righe = self.db.table('shipsteps.shorepass_righe')
      # sp_id = kwargs['record_attr']['_pkey']
      # sp = tbl_shorepass_righe.query(columns="$id", where='$shorepass_id=:s_id', s_id=sp_id).fetch()
      # list_sp=[]
      # for r in range(len(sp)):
      #     list_sp.append(sp[r][0])
        
        builder = TableTemplateToHtml(table=tbl_shorepass_righe)
        storagePath=[]
        n_pkeys=len(pkeys)
        for r in range(n_pkeys):
            nome_temp = nome_template.replace('shipsteps.shorepass_righe:','')+str(r)
            nome_file = '{cl_id}.pdf'.format(
                        cl_id=nome_temp)

            template = self.loadTemplate(nome_template)  # nome del template
            pdfpath = self.site.storageNode('/tmp:template',nome_file)#('home:stampe_template', nome_file)
            storagePath.append(pdfpath.fullpath)
            record=pkeys[r]
            builder(record=record, template=template)
            
           
        
            #builder(record=record_id, template=template)
        
            if format_page=='A3':
                builder.page_format='A3'
                builder.page_width=427
                builder.page_height=290
            #print(x)
            filepdf=builder.writePdf(pdfpath=pdfpath)
       # print(x)  
        builder.pdf_handler.joinPdf(storagePath,'home:stampe_template/shorepass.pdf')
        shorepass = self.site.storageNode('home:stampe_template', 'shorepass.pdf' )
        self.setInClientData(path='gnr.clientprint',
                              value=shorepass.url(timestamp=datetime.now()), fired=True)
        

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('_row_count')
        fb.field('shorepass_id')
        fb.field('name')
        fb.field('surname')
        fb.field('rank')
        fb.field('nationality')
        fb.field('birth_date')
        fb.field('birth_place')
        fb.field('birth_country')
        fb.field('gender')
        fb.field('id_doc')
        fb.field('id_doc_n')
        fb.field('id_doc_state')
        fb.field('expire_id_doc')
        fb.field('expire')
        fb.field('start_time')
        fb.field('stop_time')
        fb.field('shorepass')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
