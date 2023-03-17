#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('cargoman_n')
        r.fieldcell('freight')
        r.fieldcell('destination')
        r.fieldcell('departure')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='arrival_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id')
        fb.field('freight')
        fb.field('destination')
        fb.field('departure')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromCargodocs(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        
        self.cargoTestata(bc.borderContainer(region='top',datapath='.record',height='120px'))
        self.cargoRighe(bc.contentPane(region='center'))
        #self.bunker_att(bc.contentPane(region='right',width='50%'))
    def cargoTestata(self,bc):
        center = bc.roundedGroup(title='!![en]Loading Cargo docs',region='center',width='auto',background = 'lightgrey')
        fb = center.formbuilder(cols=2, border_spacing='4px')

        #fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('cargoman_n', readOnly=True)
        fb.field('freight', width='50.5em',colspan=2)
        fb.dbSelect(dbtable='unlocode.place',lbl='!![en]Select place',columns='$descrizione,$unlocode',auxColumns='@nazione_code.nome',
                    selected_citta_nazione='.destination')
        fb.field('destination', width='25em')
        fb.field('departure')
    
    def cargoRighe(self,bc):
        left = bc.contentPane(region='center',width='500px', datapath='#FORM')
        left.inlineTableHandler(relation='@bl_cargodocs',viewResource='ViewFromBlRighe')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_cargoman,20,stampa_mates,*,10')
        btn_cm_print=bar.stampa_cargoman.button('Print Cargo Manifest')
        btn_mr_print=bar.stampa_mates.button("Print Mate's Receipt")
        btn_cm_print.dataRpc('', self.print_template,record='=#FORM.record',nome_template = 'shipsteps.cargo_docs:cargo_manifest',
        _ask=dict(title='!![en]Select the letterhead',fields=[dict(name='letterhead', lbl='!![en]Letterhead', tag='dbSelect',columns='$id',
                             hasDownArrow=True, auxColumns='$name',
                             table='adm.htmltemplate')]))
        btn_mr_print.dataRpc('', self.print_template,record='=#FORM.record',nome_template = 'shipsteps.cargo_docs:mates_receipt',
        _ask=dict(title='!![en]Select the letterhead',fields=[dict(name='letterhead', lbl='!![en]Letterhead', tag='dbSelect',columns='$id',
                             hasDownArrow=True, auxColumns='$name',
                             table='adm.htmltemplate')]))

    @public_method
    def print_template(self, record, resultAttr=None, nome_template=None,format_page=None, **kwargs):
        
        record_id=record['id']
        #verifichiamo nei kwargs se abbiamo la letterhead da passare come carta intestata 
        if kwargs:
           letterhead=kwargs['letterhead']
        else:
           letterhead=''
        tbl_sof = self.db.table('shipsteps.cargo_docs')
        builder = TableTemplateToHtml(table=tbl_sof)

        nome_temp = nome_template.replace('shipsteps.cargo_docs:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        #builder(record=selId, template=template)
        builder(record=record_id, template=template,letterhead_id=letterhead)
        if format_page=='A3':
            builder.page_format='A3'
            builder.page_width=427
            builder.page_height=290


        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)    