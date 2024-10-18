# encoding: utf-8


class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('owner',pkey='id',name_long='!![en]Owner',name_plural='!![en]Owners',caption_field='own_name')
        self.sysFields(tbl)
        tbl.column('own_name',name_short='!![en]Owner name')
        tbl.column('address_own',name_short='!![en]Owner address')
        tbl.formulaColumn('own_fullname', "$own_name || ' ' || coalesce($address_own,'')")
        #tbl.formulaColumn('own_fullname', """('<div class="wrappingcolumn">'|| $own_name || ' ' || coalesce($address_own,''||'</div>' ))""")
        #tbl.formulaColumn('descrizione_wrappata', """( '<div style="height\:fit-content;" class="wrappingcolumn">'|| $own_fullname ||'</div>' )""")
        tbl.formulaColumn('own_fullname_wrap', """( '<div class="wrappingcolumn">'|| $own_fullname ||'</div>' )""")
        #tbl.formulaColumn('descrizione_wrappata', """
        #        CASE WHEN LENGTH($own_fullname) > 70 THEN LEFT($own_fullname, 67) || '...'    
        #              ELSE $own_fullname
        #        END
        #    """)
