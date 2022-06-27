class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('extradaticp', pkey='id', name_long='!![en]Extra data CP', name_plural='!![en]Extra data CP',
                                      caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='extradatacp', mode='foreignkey', onDelete='cascade', one_one='*')
        tbl.column('lavori', name_short='Per lavori o altri motivi')
        tbl.column('notizie',  name_short='Altre notizie')
        tbl.column('pilot_arr', dtype='B', name_short='!![en]Pilot on arrival')
        tbl.column('pilot_arr_vhf', dtype='B', name_short='!![en]Pilot VHF on arrival')
        tbl.column('antifire_arr', dtype='B', name_short='!![en]Antifire on arrival')
        tbl.column('antipol_arr', dtype='B', name_short='!![en]Antipollution on arrival')
        tbl.column('moor_arr', dtype='B', name_short='!![en]Moor on arrival')
        tbl.column('n_moor_arr', name_short='!![en]No. moor on arrival')
        tbl.column('tug_arr', dtype='B', name_short='!![en]Tug on arrival')
        tbl.column('n_tug_arr', name_short='!![en]No. Tug on arrival')
        tbl.column('daywork', name_short='!![en]Days of work')
        tbl.column('timework',  name_short='!![en]Time work')
        tbl.column('pilot_dep', dtype='B', name_short='!![en]Pilot on departure')
        tbl.column('pilot_dep_vhf', dtype='B', name_short='!![en]Pilot VHF on departure')
        tbl.column('antifire_dep', dtype='B', name_short='!![en]Antifire on departure')
        tbl.column('antipol_dep', dtype='B', name_short='!![en]Antipollution on departure')
        tbl.column('moor_dep', dtype='B', name_short='!![en]Moor on departure')
        tbl.column('n_moor_dep', name_short='!![en]No. moor on departure')
        tbl.column('tug_dep', dtype='B', name_short='!![en]Tug on departure')
        tbl.column('n_tug_dep', name_short='!![en]No. Tug on departure')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')