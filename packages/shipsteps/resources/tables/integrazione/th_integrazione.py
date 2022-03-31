#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('cargo_unl_load_id')
        r.fieldcell('noleggiatore')
        r.fieldcell('place_origin_goods')
        r.fieldcell('place_dest_goods')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='cargo_unl_load_id', op='contains', val='')


class ViewIntegrazione(BaseComponent):
    
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('cargo_unl_load_id',name='Carico', edit=True, width='auto',tab='dbSelect',hasDownArrow=True,
                                        condition=":aid = $arrival_id",
                                        condition_aid='^#FORM.record.id')
        r.fieldcell('noleggiatore', edit=True, width='auto')
        r.fieldcell('place_origin_goods',auxColumns='@nazione_code.nome' , edit=True, width='20em')
        r.fieldcell('place_dest_goods',auxColumns='@nazione_code.nome' , edit=True, width='20em')
    
    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='cargo_unl_load_id', op='contains', val='')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('cargo_unl_load_id' )
        fb.field('noleggiatore' )
        fb.field('place_origin_goods' )
        fb.field('place_dest_goods' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
