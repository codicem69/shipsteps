class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('mov_type',pkey='id',name_long='mov_type',name_plural='mov_type',
                        caption_field='hierarchical_descrizione')
        self.sysFields(tbl,hierarchical='descrizione', counter=True, df=True)
        tbl.column('descrizione',name_long='!![en]Description')