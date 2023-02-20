#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent


class LookupView(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('agency_id', edit=True, hasDownArrow=True)
        r.fieldcell('garbageval')
        r.fieldcell('garbageval')
        r.fieldcell('retaingarbval')
        r.fieldcell('ispsval')
        r.fieldcell('miscval')
        r.fieldcell('bulkval')
        r.fieldcell('notemiscval')

    def th_order(self):
        return 'garbageval'

    def th_query(self):
        return dict(column='id', op='contains', val='')

