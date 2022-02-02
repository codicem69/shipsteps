#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method


class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('bln', width='7em')
        r.fieldcell('shipper_id', width='30em')
        r.fieldcell('receiver_id', width='30em')
        r.fieldcell('quantity')
        r.fieldcell('measure_id')
        r.fieldcell('description', width='20em')
        r.fieldcell('description_it', width='20em')
        r.fieldcell('operation')
        r.fieldcell('foreign_cargo')
       

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='description', op='contains', val='')

class ViewFromCargoLU(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('arrival_id')
        r.fieldcell('bln', hasDownArrow=True,edit=True, width='7em')
        r.fieldcell('shipper_id', hasDownArrow=True,edit=True, width='40em')
        r.fieldcell('receiver_id', hasDownArrow=True,edit=True, width='40em')
        r.fieldcell('quantity', edit=True, totalize=True)
        r.fieldcell('measure_id', hasDownArrow=True,edit=True, width='5em')
        r.fieldcell('description', edit=True, width='20em')
        r.fieldcell('description_it', edit=True, width='20em')
        r.fieldcell('operation', edit=True, width='5em')
        r.fieldcell('foreign_cargo', edit=True, width='5em')    



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('bln')
        fb.field('shipper_id' )
        fb.field('receiver_id' )
        fb.field('quantity' )
        fb.field('measure_id' )
        fb.field('description' )
        fb.field('description_it' )
        fb.field('operation' )
        fb.field('foreign_cargo' )
        
       

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
