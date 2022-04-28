# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('sof_operations', pkey='id', name_long='!![en]Operation SOF', name_plural='!![en]Operations SOF',
                                        caption_field='id', partition_agency_id='agency_id', order_by='date')
        self.sysFields(tbl)

        tbl.column('sof_id',size='22', name_long='sof_id'
                    ).relation('sof.id', relation_name='sof_operations', mode='foreignkey', onDelete='cascade')
        tbl.column('date', dtype='D', name_short='!![en]Date')
        tbl.column('day', name_short='!![en]Day', values='Monday:Monday,Tuesday:Tuesday,Wednesday:Wednesday,Thursday:Thursday,Friday:Friday,Saturday:Saturday,Sunday:Sunday')
        tbl.column('operations', name_short='!![en]Operations')
        tbl.column('from', dtype='H', name_short='!![en]From')
        tbl.column('to', dtype='H', name_short='!![en]To')
        tbl.aliasColumn('agency_id','@sof_id.@arrival_id.agency_id')
    
    