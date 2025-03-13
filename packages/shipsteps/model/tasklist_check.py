# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tasklist_check', pkey='id', name_long='Cheklist vessel ops', name_plural='Checklist vessel ops',caption_field='description')
        self.sysFields(tbl,counter=True)

        tbl.column('arrival_id',size='22', group='_', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='checktask_arrival', mode='foreignkey', onDelete='cascade')
        tbl.column('done', dtype='B', name_short='!![en]Done')
        tbl.column('description', name_short='!![en]Description')
        tbl.column('note', name_short='Note')