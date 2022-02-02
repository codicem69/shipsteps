#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('arrival_id')
        r.fieldcell('eosp')
        r.fieldcell('aor')
        r.fieldcell('anchored')
        r.fieldcell('anchor_up')
        r.fieldcell('pob')
        r.fieldcell('first_rope')
        r.fieldcell('moored')
        r.fieldcell('poff')
        r.fieldcell('gangway')
        r.fieldcell('free_p')
        r.fieldcell('pobd')
        r.fieldcell('last_line')
        r.fieldcell('sailed')
        r.fieldcell('cosp')

    def th_order(self):
        return 'arrival_id'

    def th_query(self):
        return dict(column='aor', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('arrival_id' )
        fb.field('eosp' )
        fb.field('aor' )
        fb.field('anchored' )
        fb.field('anchor_up' )
        fb.field('pob' )
        fb.field('first_rope' )
        fb.field('moored' )
        fb.field('poff')
        fb.field('gangway' )
        fb.field('free_p' )
        fb.field('pobd' )
        fb.field('last_line' )
        fb.field('sailed' )
        fb.field('cosp' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
