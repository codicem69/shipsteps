class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bunker_righe', pkey='id', name_long='bunker_righe', name_plural='bunker_righe',caption_field='id')
        self.sysFields(tbl)
        tbl.column('bunker_id',size='22', name_long='bunker_id'
                    ).relation('bunker.id', relation_name='bunker_righe', mode='foreignkey', onDelete='cascade')
        tbl.column('prodotto', name_short='!![en]Product/Category/Class')
        tbl.column('quantity', name_short='!![en]Quantity')
        tbl.column('zolfo', name_short='!![en]Sulfur content')
        tbl.column('punto_infiam', name_short='!![en]Flash point')
        tbl.column('denaturato', name_short='!![en]Denatured', values='SI:YES,NO:NO')