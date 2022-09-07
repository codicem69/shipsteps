class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('billoflading', pkey='id', name_long='!![en]Bill of lading', 
                        name_plural='!![en]Bill of lading',caption_field='bl_n')
        self.sysFields(tbl, counter='cargodocs_id')

        tbl.column('cargodocs_id',size='22', name_long='bl_id'
                    ).relation('cargo_docs.id', relation_name='bl_cargodocs', mode='foreignkey', onDelete='cascade')
        tbl.column('bl_n', name_short='!![en]B/L no.')
        tbl.column('shipper_id',size='22', name_long='!![en]Shippers'
                    ).relation('ship_rec.id', relation_name='shipper_bl', mode='foreignkey', onDelete='raise')
        tbl.column('consignee_id',size='22', name_long='!![en]Consignee'
                    ).relation('consignee.id', relation_name='consignee_bl', mode='foreignkey', onDelete='raise')
        tbl.column('notify_id',size='22', name_long='!![en]Notify'
                    ).relation('consignee.id', relation_name='notify_bl', mode='foreignkey', onDelete='raise')
        tbl.column('marks_n',name_short='!![en]Marks and no.')
        tbl.column('pack_n', dtype='N', name_short='!![en]No.packs')
        tbl.column('descr_goods', name_short='!![en]Description of goods')
        tbl.column('measure_id',size='22', name_long='!![en]measure'
                    ).relation('measure.id', relation_name='bl_measure', mode='foreignkey', onDelete='raise')
        tbl.column('qt_bl', dtype='N', name_short='!![en]Quantity',format='#,###.000')
        tbl.column('measure_m',size='22', name_long='!![en]measure'
                    ).relation('measure.id', relation_name='measure_extra', mode='foreignkey', onDelete='raise')
        tbl.column('measmnt', dtype='N', name_short='Measmnt',format='#,###.000')
        tbl.column('remarks', name_short='Remarks')            

        tbl.formulaColumn('scn',"""coalesce('(s): ' || @shipper_id.fullname_sr,'') || '<br>' || coalesce('(c): ' || @consignee_id.fullname_cn,'')
                                   || '<br>' || coalesce('(n): ' || @notify_id.fullname_cn,'')""" )
       