#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('data')
        r.fieldcell('reg')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='reg', op='contains', val='')



class Form(BaseComponent):
    py_requires='gnrcomponents/pagededitor/pagededitor:PagedEditor'
    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        tc = bc.tabContainer(region = 'center',margin='2px')
        self.unsealingTestata(bc.borderContainer(region='top',datapath='.record',height='100px'))
        self.unsealingRighe(tc.contentPane(region='center', title='!![en]Seals'))
        self.editUnsealing(tc.framePane(title='Edit Unsealing', datapath='#FORM.editPagine'))

    def unsealingTestata(self, pane):    
        fb = pane.div(margin_left='5px',margin_right='auto',margin_top='20px').formbuilder(cols=3, border_spacing='4px',fld_width='10em')
        fb.field('arrival_id' )
        fb.field('data' )
        fb.field('reg' )

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_unsealing,*')
        template_id = self.db.table('adm.userobject').readColumns(columns="$id",
                  where='$tbl=:tbl AND $code=:code', tbl='shipsteps.unsealing', code='unsealing')
        btn_unsealing = bar.stampa_unsealing.button('!![en]Print unsealing report',
                               action="""var tp = {template:template_id};
                               var kw = objectExtract(this.getInheritedAttributes(),"batch_*",true);
                               kw.table = 'shipsteps.unsealing';
                               kw.resource = "print_template";
                               kw.res_type = "print";
                               kw.pkey = this.form.getCurrentPkey();
                               kw.extra_parameters = new gnr.GnrBag({template_id:tp.template,table:kw.table});
                               genro.publish("table_script_run",kw)""",template_id=template_id)#sostituire il valore template_id con la variabile

    def editUnsealing(self, frame):
        bar = frame.top.slotBar('10, lett_select,*',height='20px',border_bottom='1px solid silver')
        fb = bar.lett_select.formbuilder(cols=2,datapath='#FORM.record.htmlbag_unsealing')
        fb.dbselect('^.letterhead_id',table='adm.htmltemplate',lbl='carta intestata',hasDownArrow=True)
        fb.button('Get Html Doc').dataRpc('#FORM.record.htmlbag_unsealing.source',self.db.table('shipsteps.unsealing').getHTMLDoc,
                                            unsealing_id='=#FORM.pkey',
                                            record_template='unsealing',
                                            letterhead='.letterhead_id')
        
        frame.pagedEditor(value='^#FORM.record.htmlbag_unsealing.source',pagedText='^#FORM.record.htmlbag_unsealing.output',
                          border='1px solid silver',
                          letterhead_id='^#FORM.record.htmlbag_unsealing.letterhead_id',
                          datasource='#FORM.record',printAction=True)
        
    def unsealingRighe(self,pane):
        pane.inlineTableHandler(relation='@row_unsealing',viewResource='ViewFromUnsealingRows',liveUpdate=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px', defaultPrompt=dict(title='!![en]Unsealing date', fields=self.newRecParameters(),
                    doSave=True))
    
    def newRecParameters(self):
        return [dict(value='^.data', lbl='!![en]Unsealing date',
                    validate_notnull=True, tag='dateTextBox',hasDownArrow=True)]