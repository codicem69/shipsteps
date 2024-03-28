# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('cargo_consignee', pkey='id', name_long='!![en]Cargo consignee', name_plural='!![en]Cargoes consignee',caption_field='name',lookup=True)
        self.sysFields(tbl)
        
        tbl.column('name', name_short='!![en]Name')
        tbl.column('address', name_short='!![en]Address')
        