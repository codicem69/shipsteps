#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_hiddencolumns(self):
        return '$fileurl,$is_foreign_document'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('description')
        r.fieldcell('mimetype')
        r.fieldcell('__ins_ts')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')


