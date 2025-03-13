#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('done')
        r.fieldcell('description')
        r.fieldcell('note')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='description', op='contains', val='')

class ViewFromTCheckList(BaseComponent):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em',hidden=True)
        r.fieldcell('arrival_id')
        r.fieldcell('done', edit=True)
        r.fieldcell('description', edit=True,width='70%',_customGetter="""function(row)
                        {
                         var descr_b = dataTemplate("<div><s>$description</s></div>",row);
                         var descr = dataTemplate("<div>$description</div>",row);
                         if(row.done==true) {return descr_b;}
                        else
                        return descr;
                    }""")
        r.fieldcell('note', edit=True)

    def th_order(self):
        return '_row_count'

    def th_view(self,view):
        bar = view.top.bar.replaceSlots('delrow','load_checklist,25,delrow')
        btn_checklist=bar.load_checklist.button('!![en]Load checklist ',disabled="""^#FORM.shipsteps_tasklist_check.view.count.shown""")
        btn_checklist.dataRpc('nome_temp', self.load_Checklist,record='=#FORM.record')

    @public_method
    def load_Checklist(self, record, **kwargs):
        record_id = record['id']
        movtype_id=record['movtype_id']
        tbl_checklist = self.db.table('shipsteps.checklist')
        checklist_id=tbl_checklist.readColumns(columns='$id', where='$movtype_id=:mov_id', mov_id=movtype_id)
        tbl_ckRighe = self.db.table('shipsteps.checklist_righe')
        record_ckRighe = tbl_ckRighe.query(columns="*",
                         where='$checklist_id=:ckl_id',ckl_id=checklist_id).fetch()
        
        tbl_ckArrival = self.db.table('shipsteps.tasklist_check')
        
        for r in record_ckRighe:
            if not tbl_ckArrival.checkDuplicate(arrival_id=record_id,description=r['description']):
                nuovo_rec = dict(arrival_id=record_id,done=False,description=r['description'])
                tbl_ckArrival.insert(nuovo_rec)
            
        self.db.commit() 

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('done')
        fb.field('description' )
        fb.field('note' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
