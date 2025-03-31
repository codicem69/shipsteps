#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
from gnr.app.gnrapp import GnrApp

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('emesso', margin_top='5px', semaphore=True, name=' ')
        r.fieldcell('beneficiario_id', width='30em',color="=#ROW.emesso?=#v==true?'green':'red'", name='!![en]Beneficiary')
        r.fieldcell('iban',width='15em')
        r.fieldcell('causale', width='50em')
        r.fieldcell('importo')
        r.fieldcell('imp_lettere')
        
    def th_order(self):
        return 'beneficiario_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')
    
    def th_options(self):
        return dict(grid_selfDragRows=True, grid_showLineNumber=True)

class ViewFromTributi(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('beneficiario_id', edit=dict(validate_notnull=True), name='!![en]Beneficiary', width='30em')
        r.fieldcell('causale', edit=dict(validate_notnull=True), width='50em')
        r.fieldcell('importo', edit=dict(validate_notnull=True))
        r.fieldcell('imp_lettere', edit=True)
        r.cell('_button', name='Azione',
               format_buttonclass='buttonInGrid',
               format_isbutton='Stampa Tributi', 
               format_onclick="""var row = this.widget.rowByIndex($1.rowIndex);
                                 var that = this; 
                                 genro.dlg.ask('Attenzione','Vuoi stampare i tributi?',
                                 {'cancel':'Annulla','boll':'Bollettino', 'bonifico':'Bonifico'},
                                 {boll:function(){
                                   PUBLISH esegui_azione = {tributi_id:row._pkey,row:row,tip_versamento:'bollettino'};},
                                 bonifico:function(){
                                   PUBLISH esegui_azione = {tributi_id:row._pkey,row:row,tip_versamento:'bonifico'};}})""",  
                                width='8em', text_align='center')
               
        r.fieldcell('emesso', edit=True)                                             
               
    
    def th_view(self, view):
        view.dataRpc('nome_temp', self.print_template_tributi,record='=#FORM.record',
                                    subscribe_esegui_azione=True)                              
               
    @public_method
    def print_template_tributi(self, record, resultAttr=None,selId=None, servizio=[] , format_page=None, **kwargs):
        #msg_special=None
        #print(x)
        selId=kwargs['tributi_id']
        
        versamento=kwargs['tip_versamento']
        if versamento == 'bonifico':
            nome_template = 'shipsteps.tributi_cp:bonifico'
        if versamento == 'bollettino':
            nome_template = 'shipsteps.tributi_cp:bollettino'     
        if selId is None:
            nome_temp = 'no_tributi'
            return nome_temp
        
        tbl_tributi_cp = self.db.table('shipsteps.tributi_cp')
        builder = TableTemplateToHtml(table=tbl_tributi_cp)

        nome_temp = nome_template.replace('shipsteps.tributi_cp:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)
        
        builder(record=selId, template=template)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290
        if versamento == 'bollettino':
            builder.page_format='A4'
            builder.page_width=297
            builder.page_height=210 
            builder.page_orientation='H'      
        
        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)
        
        nome_temp='tributi_cp'
        return nome_temp

class Form(BaseComponent):
    css_requires='wrapping'
    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('beneficiario_id', width='40em',lbl='!![en]Beneficiary',selected_iban='.iban')
        fb.dbSelect('^.caus',lbl='Seleziona tributi CP', width='40em',table='shipsteps.causali_tributicp',columns='$code_pi',
                    auxColumns='$uo_accertatrice,$descr_pratica_wrap,$oggetto_wrap,$sotto_oggetto_wrap',
                    selected_descrizione='.causal',selected_tariffa='.importo',selected_iban='.iban',
                    hasDownArrow=True, hidden='^.@beneficiario_id.beneficiario?=#v!=="Tesoreria dello Stato"')
        fb.dataController("if(causal) SET .causale=causal + ' ' + vess_type +' '+nome_nave", causal='^.causal',vess_type='^.@arrival_id.@vessel_details_id.@imbarcazione_id.tip_imbarcazione_code',nome_nave='^.@arrival_id.@vessel_details_id.@imbarcazione_id.nome')
        fb.field('causale',width='40em', tag='simpletextarea')
        fb.field('importo')
        fb.field('imp_lettere')
        fb.field('emesso')
        btn_trib = fb.Button('!![en]Print Tributes')
        fb.dataController("""var id = button.id;
                        if(msg=='tributi_cp') {SET .emesso=true;}
                        if (ca==true){document.getElementById(id).style.backgroundColor = 'lightgreen';}
                        else {document.getElementById(id).style.backgroundColor = '';}
                        """, ca='^.emesso',button=btn_trib.js_widget,msg='^nome_temp')                     
        btn_trib.dataRpc('nome_temp', self.print_template_tributi,record='=#FORM.record',servizio=['tributi'], 
                                format_page='A4',selId='=#FORM.shipsteps_tributi_cp.view.grid.selectedId',selPkeys_att='=#FORM.attachments.view.grid.currentSelectedPkeys',                            
                                _ask=dict(title='!![en]Select the type of payment',fields=[dict(name='tip_versamento', lbl='!![en]Type of payment', tag='filteringSelect',hasDownArrow=True,
                                values='bonifico:Bonifico,bollettino:Bollettino postale',
                                validate_notnull=True,cols=4,popup=True,colspan=2),dict(name='letterhead', lbl='!![en]Letterhead', tag='dbSelect',columns='$id',
                             hasDownArrow=True, auxColumns='$name',
                             table='adm.htmltemplate')]),_onResult="this.form.save()")
        dlg = pane.dialog(nodeId='dialog_poste',parentRatio=1,title='Times',closable=True,subscribe_closeDialog_ws="this.widget.hide();")
        bc = dlg.borderContainer()
        top = bc.contentPane(region='top', height='100%')
        top.htmliframe(src="""https://pagamenti.poste.it/""",
                                                    height='100%',width='100%',border='0px')
        #fb.button('Sito Poste', action="genro.wdgById('dialog_poste').show()")
        
        fb.button('Sito Poste pagamenti',action='genro.openBrowserTab(link_poste)',link_poste = self.db.application.getPreference('link_poste',pkg='shipsteps'))
        #btn_app=fb.button('testapp')
        #btn_app.dataRpc('datiapp', self.testapp,record='=#FORM.record',_ask="Attenzione confermi l'addebito sulla carta?")

    def th_options(self):
        return dict(parentRatio=1)
        #return dict(dialog_height='400px', dialog_width='800px')

    #@public_method
    #def testapp(self,record=None,**kwargs):
    #    vess_type=record['@arrival_id.@vessel_details_id.@imbarcazione_id.nome']
    #    nome_imb=record['@arrival_id.@vessel_details_id.@imbarcazione_id.nome']
    #    causale='Tributi '+record['causale']
    #    num_carta = self.db.application.getPreference('carta',pkg='shipsteps')
    #    app_carte = GnrApp('carte')
    #    db_carte = app_carte.db
    #    tbl_mov = db_carte.table('carte.movimenti')
    #    myquery = tbl_mov.query(columns="$descrizione",
    #              where='@carta_id.num_carta = :carta',
    #              carta=num_carta).fetch()
    #    
    #    print(x)

    @public_method
    def print_template_tributi(self, record, resultAttr=None,selId=None, servizio=[] , format_page=None, **kwargs):
       
        selId=record['id']
        versamento=kwargs['tip_versamento']
        if versamento == 'bonifico':
            nome_template = 'shipsteps.tributi_cp:bonifico'
        if versamento == 'bollettino':
            nome_template = 'shipsteps.tributi_cp:bollettino'     
        if selId is None:
            nome_temp = 'no_tributi'
            return nome_temp
        
        #verifichiamo nei kwargs se abbiamo la letterhead da passare come carta intestata 
        if kwargs:
           letterhead=kwargs['letterhead']
        else:
           letterhead=''

        tbl_tributi_cp = self.db.table('shipsteps.tributi_cp')
        builder = TableTemplateToHtml(table=tbl_tributi_cp)

        nome_temp = nome_template.replace('shipsteps.tributi_cp:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)
        
        builder(record=selId, template=template,letterhead_id=letterhead)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290
        if versamento == 'bollettino':
            builder.page_format='A4'
            builder.page_width=297
            builder.page_height=210 
            builder.page_orientation='H'      
        
        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)
        
        nome_temp='tributi_cp'
        return nome_temp