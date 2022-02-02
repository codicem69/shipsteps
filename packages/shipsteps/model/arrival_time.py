# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('arrival_time', pkey='id', name_long='!![en]arrival times', name_plural='!![en]arrival times',
                                      caption_field='aor', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='time_arr', mode='foreignkey', onDelete='cascade', one_one='*')   
        tbl.column('eosp', dtype='DH', name_short='!![en]End of sea passage')     
        tbl.column('aor', dtype='DH', name_short='!![en]Arrived on road')
        tbl.column('anchored', dtype='DH', name_short='!![en]Anchored')
        tbl.column('anchor_up', dtype='DH', name_short='!![en]Anchor up')
        tbl.column('pob', dtype='DH', name_short='!![en]Pilot on board')
        tbl.column('first_rope', dtype='DH', name_short='!![en]First rope')
        tbl.column('moored', dtype='DH', name_short='!![en]Moored')
        tbl.column('poff', dtype='DH', name_short='!![en]Pilot off')
        tbl.column('gangway', dtype='DH', name_short='!![en]Gangway in pos.')
        tbl.column('free_p', dtype='DH', name_short='!![en]Free pratique')
        tbl.column('pobd', dtype='DH', name_short='!![en]Pilot on board dep')
        tbl.column('last_line', dtype='DH', name_short='!![en]Last line')
        tbl.column('sailed', dtype='DH', name_short='!![en]Vessel sailed')
        tbl.column('cosp', dtype='DH', name_short='!![en]Commenced of sea pass')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')