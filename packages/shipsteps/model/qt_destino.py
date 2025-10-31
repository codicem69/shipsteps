# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('qt_destino', pkey='id', name_long='!![en]Daily Quantity by destination', name_plural='!![en]Daily Quantity by destination',
                      caption_field='tot_xdate')
        self.sysFields(tbl, counter='dailysof_id')
        tbl.column('dailysof_id',size='22', group='_', name_long='dailysof_id'
                    ).relation('daily_sofdetails.id', relation_name='qtdest', mode='foreignkey', onDelete='raise')
        tbl.column('wharehouse_id',size='22', group='_', name_long='!![en]Wharehouse'
                    ).relation('magazzini.id', relation_name='wharehouse', mode='foreignkey', onDelete='raise')
        tbl.column('tot_xdate', dtype='N', name_short='!![en]Total Quantity', format='#,###.000')
        
        