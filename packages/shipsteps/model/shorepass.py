class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('shorepass', pkey='id', name_long='shorepass', name_plural='shorepass',caption_field='id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='shorepass_arr', mode='foreignkey', onDelete='cascade',onDuplicate=False)
        tbl.column('data_arr', dtype='D', name_short='!![en]Arrival date')
        tbl.column('data_part', dtype='D', name_short='!![en]Departure date')
       
        #tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.formulaColumn('data_attuale',"""CASE WHEN $arrival_id <> ''THEN :currdate END""",var_currdate=self.db.workdate)

