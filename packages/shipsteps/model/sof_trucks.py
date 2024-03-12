# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('sof_trucks', pkey='id', name_long='!![en]Transport detail', name_plural='!![en]Transport details',
                      caption_field='id', order_by='_row_count')
        self.sysFields(tbl, counter='sof_id')
        tbl.column('sof_id',size='22', name_long='sof_id'
                    ).relation('sof.id', relation_name='sof_trucks', mode='foreignkey', onDelete='cascade')
        tbl.column('date', dtype='D', name_short='!![en]Date')
        tbl.column('targa', name_short='!![en]Truck plate')
        tbl.column('tara', dtype='I', name_short='!![en]Tare Kg')
        tbl.column('lordo', dtype='I', name_short='!![en]Gross Kg')
        tbl.column('netto', dtype='I', name_short='!![en]Net Kg')
        tbl.column('total', dtype='I', name_short='!![en]Progressive Kg')
        tbl.aliasColumn('workport', '@sof_id.@arrival_id.workport')