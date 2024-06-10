# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('garbage_details', pkey='id', name_long='!![en]Garbage detail', name_plural='!![en]Garbage detail',caption_field='tip_garbage_id')
        self.sysFields(tbl)

        tbl.column('garbage_id',size='22', group='_', name_long='garbage_id'
                    ).relation('garbage.id', relation_name='garbage_arr', mode='foreignkey', onDelete='raise')
        tbl.column('tip_garbage_id',size='22', group='_', name_long='!![en]Garbage type'
                    ).relation('tip_garbage.id', relation_name='tipgarb', mode='foreignkey', onDelete='raise')
        tbl.column('measure', name_short='!![en]Measure')
        tbl.column('quantity', name_short='!![en]Quantity')
        