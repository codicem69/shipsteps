# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('unsealing_righe', pkey='id', name_long='!![en]Unsealing row', name_plural='!![en]Unsealing rows',caption_field='seals')
        self.sysFields(tbl,counter='unsealing_id')

        tbl.column('unsealing_id',size='22', group='_', name_long='unsealing_id'
                    ).relation('unsealing.id', relation_name='row_unsealing', mode='foreignkey', onDelete='cascade')
        #tbl.column('position_id',size='22', group='_', name_long='position_id'
        #            ).relation('seal_position.id', relation_name='position_seal', mode='foreignkey', onDelete='raise')
        tbl.column('position', name_short='Position')
        tbl.column('seals', name_short='!![en]Seal no.')