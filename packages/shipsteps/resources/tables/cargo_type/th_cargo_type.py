#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('parent_id')
        r.fieldcell('descrizione')
        r.fieldcell('hierarchical_descrizione')
        r.fieldcell('_parent_h_descrizione')
        r.fieldcell('hierarchical_pkey')
        r.fieldcell('_parent_h_pkey')
        r.fieldcell('_h_count')
        r.fieldcell('_parent_h_count')
        r.fieldcell('_row_count')
        r.fieldcell('df_fields')
        r.fieldcell('df_fbcolumns')
        r.fieldcell('df_custom_templates')
        r.fieldcell('df_colswidth')

    def th_order(self):
        return 'parent_id'

    def th_query(self):
        return dict(column='parent_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top',datapath='.record').formbuilder(cols=2, border_spacing='4px')
        fb.field('descrizione',validate_notnull=True)
        tc = bc.tabContainer(region='center')
        th = tc.contentPane(title='!![en]Cargo type').plainTableHandler(relation='@cargotype',pbl_classes=True,
                                                                margin='2px')
        form.htree.relatedTableHandler(th, dropOnRoot=False, inherited=True)

       # pane = form.record
       #fb = pane.formbuilder(cols=2, border_spacing='4px')
       #fb.field('parent_id')
       #fb.field('descrizione')
       #fb.field('hierarchical_descrizione')
       #fb.field('_parent_h_descrizione')
       #fb.field('hierarchical_pkey')
       #fb.field('_parent_h_pkey')
       #fb.field('_h_count')
       #fb.field('_parent_h_count')
       #fb.field('_row_count')
       #fb.field('df_fields')
       #fb.field('df_fbcolumns')
       #fb.field('df_custom_templates')
       #fb.field('df_colswidth')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
