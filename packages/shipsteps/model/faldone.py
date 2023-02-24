class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('faldone', pkey='id', name_long='Faldone', 
                        name_plural='Faldoni',caption_field='numero')
        self.sysFields(tbl,counter=True)
        tbl.column('numero', name_short='!![en]Number')

        tbl.column('dal', dtype='D', name_long='!![en]Date from')
        tbl.column('al', dtype='D', name_long='!![en]Date to')
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))

    
