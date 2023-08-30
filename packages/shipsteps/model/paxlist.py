class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('paxlist', pkey='id', name_long='paxlist', name_plural='paxlist',caption_field='id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='paxlist_arr', mode='foreignkey', onDelete='cascade',onDuplicate=False)
        tbl.column('data_arr', dtype='D', name_short='!![en]Arrival date')
        tbl.column('data_part', dtype='D', name_short='!![en]Departure date')
        tbl.column('arr_dep', dtype='T', name_short='!![en]Arrival/Departure')