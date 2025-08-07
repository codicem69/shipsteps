class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('seal_position', pkey='id', name_long='!![en]Seal position', name_plural='!![en]Seals position',caption_field='description', lookup=True)
        self.sysFields(tbl)

        tbl.column('description', name_short='!![en]Description')