#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrnumber import decimalRound

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
       # r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('sof_id')
        r.fieldcell('date_op')
        r.fieldcell('measure_id')
        r.fieldcell('qt_mov')
        r.fieldcell('tot_progressivo')
        r.fieldcell('shortage_surplus')
        r.fieldcell('perc_short_surpl')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='sof_id', op='contains', val='')

class ViewFromSofDailyOp(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('sof_id')
        r.fieldcell('date_op', edit=True)#, edit=dict(tag='dbSelect', table='shipsteps.sof_operations',rowcaption='$date', condition='$sof_id=:sofid', 
                               #condition_sofid='=#FORM.record.id',alternatePkey='date', hasDownArrow=True))
        
        r.fieldcell('measure_id',edit=True, width='5em',condition="$id =:cod",condition_cod='=#FORM.record.measure_sof',validate_notnull=True)
        #r.fieldcell('qt_mov',edit=dict(remoteRowController=True))
        r.fieldcell('qt_mov',edit=True)
        r.fieldcell('totcargo')
        r.cell('tot_progressivo',formula='+=qt_mov', format='#,###.000', name='!![en]Total Quantity Handled', dtype='N')
        #r.cell('shortage_surplus',formula='totcargo-tot_progressivo', format='#,###.000',name='!![en]Shortage / Surplus', dtype='N',
        #        name_style='color:red', range_alto='value<0', range_alto_style='color:black;font-weight:bold;',range_basso='value>0',
        #        range_basso_style='font-weight:bold;color:red;')
        #r.cell('perc_short_surpl', formula='totcargo?shortage_surplus/totcargo*100:0', format='#,###.000', name='Shortage / Surplus %',dtype='N',
        #                        name_style='color:red', range_alto='value<0', range_alto_style='color:black;font-weight:bold;',range_basso='value>0',
        #                        range_basso_style='font-weight:bold;color:red;')
        r.cell('tot_progres',formula='+=qt_mov', format='#,###.000', name='!![en]Total Quantity Handled', dtype='N', hidden=True)
        r.cell('shortage',formula='-totcargo+tot_progres', format='#,###.000', name='!![en]Shortage / Surplus', dtype='N',name_style='color:red',
                          range_alto='value>0',range_alto_style='color:black;font-weight:bold;',range_basso='value<0',range_basso_style='font-weight:bold;color:red;')
        r.cell('shortage_perc',formula='shortage>=0?shortage/totcargo*100:-shortage/totcargo*100', format='#,###.000', name='Shortage / Surplus %', dtype='N', 
                               range_alto='shortage>0',range_alto_style='color:black;font-weight:bold;',range_basso='shortage<0',range_basso_style='font-weight:bold;color:red;')
        #r.fieldcell('tot_progressivo',calculated=True,width='7em',name='tot_progr', dtype='N',format='###.00',totalize=True,formula='+=qt_mov')
    
 
    #@public_method
    #def th_remoteRowController(self, row=None, field=None, **kwargs):
#
    #   tbl_sof_cargo = self.db.table('shipsteps.sof_cargo')
    #   tbl_cargo = self.db.table('shipsteps.cargo_unl_load')
#
    #   sof_id = kwargs['row_attr']['sof_id']
#
    #   cargo_id = tbl_sof_cargo.query(
    #       columns="$cargo_unl_load_id",
    #       where='$sof_id=:sof_id',
    #       sof_id=sof_id
    #   ).fetch()
#
    #   tot_cargo = 0
#
    #   for r in cargo_id:
    #       quantity = tbl_cargo.readColumns(
    #           columns='$quantity',
    #           where='$id=:cargo_id',
    #           cargo_id=r[0]
    #       ) or 0
#
    #       tot_cargo += quantity
#
    #   tot_progressivo = kwargs['row_attr'].get('tot_progres') or 0
#
    #   shortage_surplus = tot_cargo - tot_progressivo
#
    #   if tot_cargo:
    #       perc_short_surpl = decimalRound(
    #           shortage_surplus / tot_cargo * 100
    #       )
    #   else:
    #       perc_short_surpl = 0
#
    #   # IMPORTANTE: valorizziamo anche totcargo
    #   row['totcargo'] = tot_cargo
    #   row['tot_progressivo'] = tot_progressivo
    #   row['shortage_surplus'] = shortage_surplus
    #   row['perc_short_surpl'] = perc_short_surpl
#
    #   return row
    
    @public_method
    def th_remoteRowController(self,row=None,field=None,**kwargs):
        
        field=field
        tbl_sof_cargo = self.db.table('shipsteps.sof_cargo')
        sof_id=kwargs['row_attr']['sof_id']
        cargo_id = tbl_sof_cargo.query(columns="$cargo_unl_load_id",
                                        where='$sof_id=:sof_id',sof_id=sof_id).fetch()   
        n_cargo = len(cargo_id) 
        tot_cargo=0        
        tbl_cargo = self.db.table('shipsteps.cargo_unl_load')                                                       
        for r in range (n_cargo):
            tot_cargo += tbl_cargo.readColumns(columns='$quantity', where='$id=:cargo_id', cargo_id=cargo_id[r][0])
        
        tot_progressivo = kwargs['row_attr']['tot_progres']
        shortage_surplus = float(tot_cargo) - float(tot_progressivo)
        perc_short_surpl = shortage_surplus/float(tot_cargo)*100
        row['totcargo'] = tot_cargo
        row['tot_progressivo']=tot_progressivo
        row['shortage_surplus']=shortage_surplus
        row['perc_short_surpl']=perc_short_surpl
        return row

    def th_order(self):
        return '_row_count'
    
    def th_options(self):
        return dict(grid_selfDragRows=True)


    def th_view(self,view):
        bar = view.top.bar.replaceSlots('delrow','reload,5,delrow')
        bar.reload.button('!![en]Reload',
                         iconClass='iconbox reload',width='8em',
                         action="this.form.reload();")
    
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('sof_id')
        fb.field('date_op')
        fb.field('measure_id')
        fb.field('qt_mov')
        fb.field('tot_progressivo')
        fb.field('shortage_surplus')
        fb.field('perc_short_surpl')
        

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
