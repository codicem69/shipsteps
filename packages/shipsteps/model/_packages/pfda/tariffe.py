# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('tariffe',partition_agency_id='agency_id')
        tbl.column('agency_id',size='22', name_long='!![en]agency',batch_assign=True,plugToForm=True
                    ).relation('shipsteps.agency.id', relation_name='agency_tariffe', mode='foreignkey', onDelete='setNull')

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))
