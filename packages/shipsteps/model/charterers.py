class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('charterers', pkey='id', name_long='!![en]Charterers', name_plural='Charterers',caption_field='fullname_chrts')
        self.sysFields(tbl,counter=True)

        tbl.column('name', name_short='!![en]Name')
        tbl.column('address', name_short='!![en]Address')
        tbl.column('city', name_short='!![en]City-Place')
        tbl.formulaColumn('fullname_chrts',"$name || ', ' || coalesce($address, '') || ', ' || coalesce($city, '')")