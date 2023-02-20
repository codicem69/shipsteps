class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('cargo_type',pkey='id',name_long='cargo_type',name_plural='cargo_type',
                        caption_field='hierarchical_descrizione')
        self.sysFields(tbl,hierarchical='descrizione', counter=True, df=True)
        tbl.column('descrizione',name_long='!![en]Description')