#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('movement_ts')
        r.fieldcell('dock_from_id')
        r.fieldcell('dock_to_id')
        r.fieldcell('pilot')
        r.fieldcell('moor')
        r.fieldcell('tug')
        r.fieldcell('num_tug')
        r.fieldcell('reason')
        r.fieldcell('note')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')




class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('movement_ts' )
        fb.field('dock_from_id',width='20em' )
        fb.field('dock_to_id',width='20em' )
        fb.field('reason' , width='60em',tag='simpleTextArea')
        div_service=pane.div(width='auto',height='30%',margin='auto',
                        padding='2px',
                        border='1px solid silver',
                        margin_top='1px',margin_left='6px',margin_right='6px')
        fb_s = div_service.formbuilder(cols=1, border_spacing='4px')
        fb_s.div('<center><strong>SERVIZI APPLICATI</strong>')
        fb_s.field('pilot')
        fb_s.field('moor')
        fb_s.field('tug')
        fb_s.field('num_tug', width='3em',validate_notnull='^#FORM.record.tug')
        
        fb_s.field('note', tag='simpleTextArea',width='60em' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )

    