# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('dock', pkey='id', name_long='!![en]Dock', name_plural='!![en]Docks',caption_field='dock_name', partition_port='port', 
                              lookup=True)
        self.sysFields(tbl)

        tbl.column('dock_name', name_short='!![en]Dock name')
        tbl.column('port',size='22',name_short='!![en]Port').relation('unlocode.place.id',relation_name='port_dock_unlocode', 
                                                                        mode='foreignkey', onDelete='raise')