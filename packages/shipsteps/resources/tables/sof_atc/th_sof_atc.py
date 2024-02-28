#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewFromSofAtc(BaseComponent):

    def th_hiddencolumns(self):
        return '$fileurl,$is_foreign_document'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('description', edit=True)
        r.fieldcell('mimetype')
        #r.fieldcell('filepath')

    def th_order(self):
        return '_row_count'
    
    def th_query(self):
        return dict(column='_row_count', op='contains', val='')

    def th_options(self):
        return dict(grid_selfDragRows=True)
