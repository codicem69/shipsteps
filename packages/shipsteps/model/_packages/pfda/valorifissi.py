class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('valorifissi',partition_agency_id='agency_id')
        tbl.column('agency_id',size='22', name_long='!![en]agency',plugToForm=True
                    ).relation('shipsteps.agency.id', relation_name='agency_vf', mode='foreignkey', onDelete='setNull')