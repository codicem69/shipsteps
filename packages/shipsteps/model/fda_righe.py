# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fda_righe', pkey='id', name_long='!![en]Row FDA', name_plural='!![en]Rows FDA',caption_field='prot_arr')
        self.sysFields(tbl, counter='fda_id')
        tbl.column('fda_id',size='22', name_long='fda_id'
                    ).relation('fda.id', relation_name='fda_righe', mode='foreignkey', onDelete='cascade')
        tbl.column('services_id',size='22', group='_', name_long='!![en]Service'
                    ).relation('services.id', relation_name='servizi_fda', mode='foreignkey', onDelete='raise')
        tbl.column('description', name_long='!![en]Description', name_short='!![en]Description')
        tbl.column('importo_pfda', dtype='N', name_long='!![en]PFDA Amount', name_short='!![en]PFDA Amount',format='€ #,###.00')
        tbl.column('inv_n', name_long='!![en]Invoice no.', name_short='!![en]Invoices no.')
        tbl.column('data_inv', dtype='D', name_long='!![en]Invoice date', name_short='!![en]Invoice date')
        tbl.column('importo', dtype='N', name_long='!![en]Amount', name_short='!![en]Amount',format='€ #,###.00')
        tbl.aliasColumn('prot_arr','@fda_id.@arrival_id.reference_num')