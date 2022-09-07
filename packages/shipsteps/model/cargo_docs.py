class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('cargo_docs', pkey='id', name_long='!![en]Loading Cargo docs', 
                        name_plural='!![en]Loading Cargo docs',caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl,counter=True)
        tbl.column('cargoman_n',dtype='T', name_short='!![en]Cargo man.n.')
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='cargodocs_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('freight', name_short='!![en]Freight')
        tbl.column('destination', name_short='!![en]Place of destination')
        tbl.column('departure', dtype='D', name_short='!![en]Departure date')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.aliasColumn('measure_bl','@bl_cargodocs.measure_id')
        tbl.formulaColumn('tot_qt_bl',select=dict(table='shipsteps.billoflading',
                                                columns='SUM($qt_bl)',
                                                where='$cargodocs_id=#THIS.id'),
                                    dtype='N',name_long='Tot. qt_bl',format='#,###.000')
        tbl.formulaColumn('tot_measmnt',select=dict(table='shipsteps.billoflading',
                                                columns='SUM($measmnt)',
                                                where='$cargodocs_id=#THIS.id'),
                                    dtype='N',name_long='Tot. measmnt',format='#,###.000')
        
    def counter_cargoman_n(self,record=None):
        return dict(format='$K/$NNN',code='CM', showOnLoad=True)      

    
