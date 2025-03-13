# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('checklist_righe', pkey='id', name_long='checklist righe', name_plural='checklist righe',caption_field='description')
        self.sysFields(tbl,counter='checklist_id')

        tbl.column('checklist_id',size='22', group='_', name_long='checklist_id'
                    ).relation('checklist.id', relation_name='cecklist_righe', mode='foreignkey', onDelete='cascade')
        tbl.column('description', name_short='!![en]Description')
        