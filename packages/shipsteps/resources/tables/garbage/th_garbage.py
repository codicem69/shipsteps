#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('ora_arr')
        r.fieldcell('data_arr')
        r.fieldcell('sosta_gg')
        r.fieldcell('rif_alim')
        r.fieldcell('bilge')
        r.fieldcell('cargo_res')
        r.fieldcell('altro')
        r.fieldcell('altro_spec')
        r.fieldcell('invio_fat')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromGarbage(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('ora_arr', edit=dict(validate_notnull=True))
        r.fieldcell('data_arr', edit=dict(validate_notnull=True))
        r.fieldcell('sosta_gg', edit=dict(validate_notnull=True))
        r.fieldcell('rif_alim', edit=True)
        r.fieldcell('bilge', edit=True)
        r.fieldcell('cargo_res', edit=True)
        r.fieldcell('altro', edit=True)
        r.fieldcell('altro_spec', edit=True, width='25em')
        r.fieldcell('invio_fat', edit=True, width='40em')
        
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('ora_arr' )
        fb.field('data_arr' )
        fb.field('sosta_gg' )
        fb.field('rif_alim' )
        fb.field('bilge' )
        fb.field('cargo_res' )
        fb.field('altro' )
        fb.field('altro_spec' )
        fb.field('invio_fat' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
