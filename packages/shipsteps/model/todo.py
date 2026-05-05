class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('todo', pkey='id', name_long='Todo', name_plural='Todo')
        
        self.sysFields(tbl)
        
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='todo_arr', mode='foreignkey', onDelete='cascade',onDuplicate=False)
        tbl.column('title', name_long='Titolo')
        tbl.column('description', 'T', name_long='Descrizione')
        
        tbl.column('due_date', 'DH', name_long='Scadenza')
        tbl.column('done', 'B', name_long='Completato')
        
        tbl.column('remind_at', 'DH', name_long='Ricorda il')
        tbl.column('snooze_until', 'DH', name_long='Posticipato fino a')