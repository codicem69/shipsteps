# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('shipdoc_pmis', pkey='id', name_long='!![en]Ship docs PMIS', name_plural='!![en]Ship docs PMIS',caption_field='description')
        self.sysFields(tbl)

        tbl.column('description', name_short='!![en]Description')
        