# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('causali_tributicp', pkey='id', name_long='Causale tributi CP', name_plural='Causali tributi CP',caption_field='code_pi',lookup=True)
        self.sysFields(tbl)

        tbl.column('uo_accertatrice', name_short='U.O. accertatrice')
        tbl.column('descr_pratica', name_short='Descrizione pratica')
        tbl.column('code_pi', name_short='Codificazione P.I.')
        tbl.column('oggetto', name_short='Oggetto')
        tbl.column('sotto_oggetto', name_short='Sotto descrizione oggetto')
        tbl.column('tariffa', dtype='N', name_short='Tariffa', format='#,###.00')
        tbl.column('note', name_short='Note')
        tbl.column('norma', name_short='Norma')
        tbl.column('capitolo', name_short='Capitolo entrata')
        tbl.column('iban', size='0:27', name_short='Iban')
        tbl.column('extra_descr', name_short='Descrizione aggiuntiva')
        tbl.formulaColumn('descr_pratica_wrap', """( '<div class="wrappingcolumn">'|| $descr_pratica ||'</div>' )""")
        tbl.formulaColumn('oggetto_wrap', """( '<div class="wrappingcolumn">'|| $oggetto ||'</div>' )""")
        tbl.formulaColumn('sotto_oggetto_wrap', """( '<div class="wrappingcolumn">'|| $sotto_oggetto ||'</div>' )""")
        tbl.formulaColumn('descrizione',"$code_pi || ' - ' || $capitolo")
        
        