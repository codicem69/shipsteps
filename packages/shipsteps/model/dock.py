# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('dock', pkey='id', name_long='!![en]Dock', name_plural='!![en]Docks',caption_field='dock_name', 
                              lookup=True)
        self.sysFields(tbl)

        tbl.column('dock_name', name_short='!![en]Dock name')
        