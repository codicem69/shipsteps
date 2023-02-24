# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('daily_sofdetails', pkey='id', name_long='!![en]Daily sof detail', name_plural='!![en]Daily sof details',caption_field='sof_id',
                        order_by='_row_count')
        self.sysFields(tbl, counter='sof_id')
        
        tbl.column('sof_id',size='22', name_long='sof_id'
                    ).relation('sof.id', relation_name='sof_daily', mode='foreignkey', onDelete='cascade')
        tbl.column('date_op', dtype='D', name_short='!![en]Date')
        tbl.column('measure_id',size='22', name_long='!![en]measure'
                    ).relation('measure.id', relation_name='sofdaily_measure', mode='foreignkey', onDelete='raise')
        tbl.column('qt_mov', dtype='N', name_short='!![en]Quantity handled', format='#,###.000')
        tbl.column('tot_progressivo', dtype='N', name_short='!![en]Progressive Total quantity handled', format='#,###.000')
        tbl.column('shortage_surplus', dtype='N', name_short='!![en]Q.ty Shortage / Surplus', format='#,###.000')
        tbl.column('perc_short_surpl', dtype='N', name_short='!![en]Percentage Shortage / Surplus', format='#,###.000')
        #tbl.aliasColumn('totcargo','@sof_id.tot_cargo_sof', dtype='N', format='#,###.000')
        #tbl.aliasColumn('agency_id','@sof_id.@arrival_id.agency_id')
        tbl.formulaColumn('daily_mov',"""'daily cargo discharged  -' || @measure_id.description || ' ' || $qt_mov || '<br>' ||
                                         'total cargo discharged   ' || @measure_id.description || ' ' || $tot_progressivo || '<br>' ||
                                         'remain to be discharged ' || @measure_id.description || ' ' || $shortage_surplus """)
        
        tbl.formulaColumn('totcargo',select=dict(table='shipsteps.cargo_unl_load',
                                                columns='SUM($quantity)',
                                                where='$id=#THIS.@sof_id.@sof_cargo_sof.cargo_unl_load_id'),
                                    dtype='N',name_long='!![en]Cargo total', format='#,###.000')
