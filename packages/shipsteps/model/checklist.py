# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('checklist', pkey='id', name_long='!![en]Checlist', name_plural='!![en]Checklist',caption_field='movtype_id')
        self.sysFields(tbl)
        tbl.column('movtype_id',size='22', group='_', name_long='!![en]Movements type'
                    ).relation('mov_type.id', relation_name='movtype_check', mode='foreignkey', onDelete='raise')
        tbl.column('description', name_short='!![en]Description')