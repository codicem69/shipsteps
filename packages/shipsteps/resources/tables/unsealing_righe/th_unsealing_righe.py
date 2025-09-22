#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('unsealing_id')
        r.fieldcell('position')
        r.fieldcell('seals')

    def th_order(self):
        return 'unsealing_id'

    def th_query(self):
        return dict(column='seals', op='contains', val='')

class ViewFromUnsealingRows(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('unsealing_id',edit=True)
        sealposition =  [r['description'] for r in self.db.table('shipsteps.seal_position').query(columns='$description',distinct=True).fetch()]
        r.fieldcell('position', values=','.join(sealposition),
                              edit=True,width='50%',hasArrowDown=True)
        #r.fieldcell('position_id',edit=True,width='50%')
        r.fieldcell('seals',edit=True,width='50%')

    def th_order(self):
        return 'unsealing_id'

    def th_query(self):
        return dict(column='seals', op='contains', val='')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('unsealing_id' )
        fb.field('position' )
        fb.field('seals' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
