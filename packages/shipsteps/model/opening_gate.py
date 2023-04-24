# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('opening_gate', pkey='id', name_long='!![en]Opening gate', name_plural='!![en]Opening gates',caption_field='port')
        self.sysFields(tbl)
        tbl.column('details', name_short='!![en]Details')
        tbl.column('map', dtype='P', name_short='!![en]Map')

        