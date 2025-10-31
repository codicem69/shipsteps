# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('magazzini', pkey='id', name_long='!![en]Wharehouse', name_plural='!![en]Wharehouses',caption_field='descrizione',lookup=True)
        self.sysFields(tbl)
        tbl.column('descrizione', name_long='!![en]Description', name_short='!![en]Description')
        