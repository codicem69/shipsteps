#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
from gnr.core.gnrlang import GnrException

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('paxlist_id')
        r.fieldcell('name')
        r.fieldcell('surname')
        r.fieldcell('nationality')
        r.fieldcell('birth_date')
        r.fieldcell('birth_place')
        r.fieldcell('birth_country')
        r.fieldcell('gender')
        r.fieldcell('id_doc')
        r.fieldcell('id_doc_n')
        r.fieldcell('id_doc_state')
        r.fieldcell('expire_id_doc')
        r.fieldcell('port_embark')
        r.fieldcell('port_disembark')
        r.fieldcell('transit')
        r.fieldcell('visa_n')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')

class ViewFromPaxRighe(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('paxlist_id', edit=True)
        r.fieldcell('name', edit=True)
        r.fieldcell('surname', edit=True)
        r.fieldcell('nationality', edit=dict(hasDownArrow=True),batch_assign=True)
        r.fieldcell('birth_date', edit=True, width='7em')
        r.fieldcell('birth_place', edit=True, width='7em')
        r.fieldcell('birth_country', edit=dict(hasDownArrow=True),batch_assign=True)
        r.fieldcell('gender', edit=True, width='7em')
        r.fieldcell('id_doc', edit=True)
        r.fieldcell('id_doc_n', edit=True)
        r.fieldcell('id_doc_state', edit=dict(hasDownArrow=True),batch_assign=True)
        r.fieldcell('expire_id_doc', edit=True, width='7em')
        r.fieldcell('port_embark', edit=True,width='7em',batch_assign=True)
        r.fieldcell('port_disembark', edit=True, width='7em',batch_assign=True)
        r.fieldcell('transit', edit=True, width='5em')
        r.fieldcell('visa_n', edit=True)
    
    def th_view(self,view):
        bar = view.top.bar.replaceSlots('addrow','addrow,resourcePrints,10,importa_pax,10,batchAssign,10,stampa_pax')
        btn_importa_crew = bar.importa_pax.paletteImporter(paletteCode='xls_importer',
                            dockButton_iconClass=False,
                            title='!!Importa pax',
                            importButton_label='Importa pax',
                            previewLimit=50,
                            dropMessage='Trascina qui il tuo file o clicca per cercarlo', filetype='excel',
                            importButton_action="genro.publish('import_pax',{filepath:imported_file_path})",
                            matchColumns='*')
        btn_printpax=bar.stampa_pax.button('Stampa Paxlist', iconClass='print',
                                        action="""genro.publish("table_script_run",{table:"shipsteps.paxlist",
                                                                                   res_type:'print',
                                                                                   resource:'stampa_paxlist',
                                                                                   pkey: pkey})""",
                                                                                   pkey='=#FORM.pkey')
        #btn_print_paxlist=bar.stampa_paxlist.button('Stampa Pax List')
        bar.dataRpc(self.importaPax, subscribe_import_pax=True,record='=#FORM.record',
                      _onResult="genro.publish('xls_importer_onResult',result);this.form.reload();",
                      _onError="genro.publish('xls_importer_onResult',{error:error});")
        #btn_print_paxlist.dataRpc('nome_temp', self.print_paxlist,record='=#FORM.record',vessel_name='=#FORM.record.@arrival_id.@vessel_details_id.@imbarcazione_id.nome',
        #                    nome_template = 'shipsteps.paxlist:paxlist',format_page='A4',_lockScreen=dict(message='Please Wait'))
        

    @public_method
    def importaPax(self, filepath=None, record=None, **kwargs):
        "Importa Excel pax list con nazioni"
        paesi =    self.db.table('unlocode.nazione').query(columns='$nome,$code').fetchAsDict('code')        
        reader = self.utils.getReader(filepath)
        result = Bag()
        paxlistid = record['id']
        
        for row in reader():
            if row['nationality']: 
                if len(row['nationality']) > 2:
                    raise GnrException('Nationality unlocode max 2 letters')
                paese_id = paesi.get(row['nationality']).get('code') 
            else: 
                paese_id = None 
            if row['birth_country']:
                if len(row['birth_country']) > 2:
                    raise GnrException('Birth Country unlocode max 2 letters')
                birthcountry = paesi.get(row['birth_country']).get('code')
            else:
                birthcountry = None
            if row['doc_state']:
                if len(row['doc_state']) > 2:
                    raise GnrException('Doc. State unlocode max 2 letters')
                stateid = paesi.get(row['doc_state']).get('code')
            else:
                stateid = None

            new_pax = self.db.table('shipsteps.paxlist_righe').newrecord(paxlist_id=paxlistid,nome=row['name'],cognome=row['surname'],nazionalita=paese_id,
                        data_nascita=row['birth_date'],luogo_nascita=row['birth_place'],paese_nascita=birthcountry,
                        sesso=row['gender'],id_doc=row['identity_doc'],id_doc_n=str(row['doc_n']),id_doc_state=stateid,
                        expire_id_doc=row['expire_doc'],portembark=row['port_embark'],portdisembark=row['port_disembark'],transitvisa=row['transit'],
                        visa=row['visa_n'], **row)
            
            self.db.table('shipsteps.paxlist_righe').insert(new_pax)
            result.addItem('inserted_row', row)
            
        self.db.commit()
        return result
    
    #@public_method
    #def print_paxlist(self, record, resultAttr=None, nome_template=None,vessel_name=None, format_page=None, **kwargs):
    #    record_id=record['id']
    #    
    #    tbl_shorepass = self.db.table('shipsteps.paxlist')
    #    builder = TableTemplateToHtml(table=tbl_shorepass)
    #    nome_nave = vessel_name.replace(' ', '_')
    #    nome_temp = nome_template.replace('shipsteps.paxlist:','')
    #    nome_file = '{cl_id}.pdf'.format(
    #                cl_id='pax_list_' + nome_nave)
#
    #    template = self.loadTemplate(nome_template)  # nome del template
    #    pdfpath = self.site.storageNode('home:stampe_template', nome_file)
#
    #    tbl_htmltemplate = self.db.table('adm.htmltemplate')
    #    templates= tbl_htmltemplate.query(columns='$id,$name', where='').fetch()
    #    letterhead=''       
    #    for r in range(len(templates)):
    #        if templates[r][1] == 'A4_orizz':
    #            letterhead = templates[r][0]    
    #        if format_page=='A3':
    #            if templates[r][1] == 'A3_orizz':
    #                letterhead = templates[r][0]
    #      
    #    builder(record=record_id, template=template,letterhead_id=letterhead)
    #  
    #    result = builder.writePdf(pdfpath=pdfpath)
#
    #    self.setInClientData(path='gnr.clientprint',
    #                          value=result.url(timestamp=datetime.now()), fired=True)
        
    def th_order(self):
        return '_row_count'
    
    def th_hiddencolumns(self):
        return "$_row_count"

    def th_options(self):
        return dict(grid_selfDragRows=True)
    
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('paxlist_id' )
        fb.field('name' )
        fb.field('surname' )
        fb.field('nationality' )
        fb.field('birth_date' )
        fb.field('birth_place' )
        fb.field('birth_country' )
        fb.field('gender' )
        fb.field('id_doc' )
        fb.field('id_doc_n' )
        fb.field('id_doc_state' )
        fb.field('expire_id_doc' )
        fb.field('port_embark' )
        fb.field('port_disembark' )
        fb.field('transit' )
        fb.field('visa_n' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
