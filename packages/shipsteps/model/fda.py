# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fda', pkey='id', name_long='!![en]Final DA', name_plural='!![en]Final DA',caption_field='pfda_intfat')
        self.sysFields(tbl)
        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='fda_arr', mode='foreignkey', onDelete='cascade',onDuplicate=False)
        tbl.column('pfda_id',size='22',name_short='!![en]Pfda no.').relation('pfda.proforma.id',relation_name='pfda_fda', mode='foreignkey', onDelete='raise')
        tbl.column('invoice_det_id',size='22', name_long='!![en]Invoicing'
                    ).relation('invoice_det.id', relation_name='inv_fda', mode='foreignkey', onDelete='raise')
        tbl.aliasColumn('int_fat','@invoice_det_id.fullname')
        tbl.aliasColumn('prot_pfda','@pfda_id.protocollo')
        tbl.formulaColumn('pfda_intfat',"coalesce($prot_pfda || ' - ','') || coalesce($int_fat, '')")
        tbl.formulaColumn('tot_pfda',select=dict(table='shipsteps.fda_righe',
                                                columns='SUM($importo_pfda)',
                                                where='$fda_id=#THIS.id'),
                                    dtype='N',name_long='Tot.PFDA',format='€ #,###.00')
        tbl.formulaColumn('tot_fda',select=dict(table='shipsteps.fda_righe',
                                                columns='SUM($importo)',
                                                where='$fda_id=#THIS.id'),
                                    dtype='N',name_long='Tot.FDA',format='€ #,###.00')