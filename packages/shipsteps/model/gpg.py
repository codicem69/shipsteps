# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('gpg', pkey='id', name_long='GPG', name_plural='GPG',caption_field='id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id',unique=True
                    ).relation('arrival.id', relation_name='gpg_arr', mode='foreignkey', onDelete='cascade', one_one='*',onDuplicate=False)
        tbl.column('date_start', dtype='DH', name_short='!![en]Start date hour')
        tbl.column('date_end', dtype='DH', name_short='!![en]End date hour')
        tbl.column('n_gpg', size=':2', name_short='GPG no.')
        #tbl.aliasColumn('agency_id','@arrival_id.agency_id')

    
