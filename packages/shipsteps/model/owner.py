# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('owner',pkey='id',name_long='!![en]Owner',name_plural='!![en]Owners',caption_field='own_name')
        self.sysFields(tbl)
        tbl.column('own_name',name_short='!![en]Owner name')
        tbl.column('address_own',name_short='!![en]Owner address')
        tbl.formulaColumn('own_fullname', "$own_name || ' ' || coalesce($address_own,'')")