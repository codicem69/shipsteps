#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count')
        r.fieldcell('bl_n')
        r.fieldcell('shipper_id',width='30em')
        r.fieldcell('consignee_id',width='30em')
        r.fieldcell('notify_id',width='30em')
        r.fieldcell('marks_n')
        r.fieldcell('pack_n')
        r.fieldcell('descr_goods')
        r.fieldcell('measure_id')
        r.fieldcell('qt_bl')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')

class ViewFromBlRighe(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count',counter=True, name='N.',width='3em')
        r.fieldcell('bl_n', edit=True, width='3em')
        r.fieldcell('shipper_id', edit=True, width='20em')
        r.fieldcell('consignee_id', edit=True, width='20em')
        r.fieldcell('notify_id', edit=True, width='20em')
        r.fieldcell('marks_n',edit=True)
        r.fieldcell('pack_n',edit=True, width='6em')
        r.fieldcell('descr_goods',edit=True, width='20em')
        r.fieldcell('measure_id',edit=True, width='6em')
        r.fieldcell('qt_bl',edit=True,totalize=True, width='8em')
        r.cell('tot_progressivo',formula='+=qt_bl', format='#,###.000', name='Tot.<br>progressivo', dtype='N')
        r.fieldcell('measure_m',edit=True, width='6em')
        r.fieldcell('measmnt',edit=True,totalize=True, width='8em')
        r.cell('tot_progr_measmnt',formula='+=measmnt', format='#,###.000', name='Tot.<br>progressivo', dtype='N')
        r.fieldcell('remarks',edit=True, width='8em')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='_row_count', op='contains', val='')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('bl_n')
        fb.field('shipper_id',width='30em')
        fb.field('consignee_id',width='30em')
        fb.field('notify_id',width='30em')
        fb.field('marks_n')
        fb.field('pack_n')
        fb.field('descr_goods')
        fb.field('measure_id')
        fb.field('qt_bl')
        fb.field('measure_m')
        fb.field('measmnt')
        fb.field('remarks')
        
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
