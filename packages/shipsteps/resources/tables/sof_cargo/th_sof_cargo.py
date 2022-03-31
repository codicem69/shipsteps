#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('sof_id')
        r.fieldcell('cargo_unl_load_id')

    def th_order(self):
        return 'sof_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromSof_Cargo(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('sof_id',name='Arrivo nave',edit=True)
        r.fieldcell('cargo_unl_load_id',name='Carico', edit=True, width='auto',tab='dbSelect',hasDownArrow=True,
                                        condition=":aid = $arrival_id",
                                        condition_aid='^#FORM.record.arrival_id')

    def th_view(self,view):
        view.grid.attributes.update(selfDragRows=True)
        
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('sof_id' )
        fb.field('cargo_unl_load_id', lbl = '!![en]Cargo', width='40em' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
