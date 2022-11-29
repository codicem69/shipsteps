class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('faldone', pkey='id', name_long='Faldone', 
                        name_plural='Faldoni',caption_field='numero', partition_agency_id='agency_id')
        self.sysFields(tbl,counter=True)
        tbl.column('numero', name_short='!![en]Number')
        tbl.column('agency_id',size='22', name_long='agency_id'
                    ).relation('agency.id', relation_name='faldone_agency_id', mode='foreignkey', onDelete='raise')
        tbl.column('dal', dtype='D', name_long='!![en]Date from')
        tbl.column('al', dtype='D', name_long='!![en]Date to')
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))

    