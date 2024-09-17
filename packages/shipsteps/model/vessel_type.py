# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('vessel_type', pkey='code', name_long='!![en]Vessel type', name_plural='!![en]Vessel types',caption_field='description',lookup=True)
        self.sysFields(tbl)

        tbl.column('code',size=':3', name_short='!![en]Code')
        tbl.column('description', name_short='!![en]Description')
        tbl.column('type', name_short='!![en]Type')
        tbl.formulaColumn('full_descr',"'('||$code||') '||$description||' ('||$type||')'")