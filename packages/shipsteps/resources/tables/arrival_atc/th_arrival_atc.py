#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewFromArrivalAtc(BaseComponent):

    def th_hiddencolumns(self):
        return '$fileurl,$is_foreign_document'

    def th_struct(self,struct):
        r = struct.view().rows()

        r.fieldcell('description', edit=True)
        r.fieldcell('att_email', edit=True)
        r.fieldcell('mimetype')
        #r.fieldcell('filepath')

    def th_order(self):
        return '__ins_ts:d'

    