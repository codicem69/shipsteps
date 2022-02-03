# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('sof', pkey='id', name_long='sof', name_plural='sof',caption_field='sof_det', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='sof_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('nor_tend', dtype='DH', name_short='!![en]NOR tendered')
        tbl.column('nor_rec', dtype='DH', name_short='!![en]NOR received')
        tbl.column('nor_acc', dtype='T', name_short='!![en]NOR accepted')
        tbl.column('ops_commenced', dtype='DH', name_short='!![en]Load/Unload commenced')
        tbl.column('ops_completed', dtype='DH', name_short='!![en]Load/Unload completed')
        tbl.column('doc_onboard', dtype='T', name_short='!![en]Documents onboard')
        tbl.column('remarks_rs', name_short='!![en]Receivers / Shippers Remarks')
        tbl.column('remarks_cte', name_short='!![en]Master Remarks')
        tbl.column('note', name_short='!![en]Note SOF')
        
        tbl.formulaColumn('sof_det',"@arrival_id.reference_num || ' - ' || @arrival_id.date || ' - ' || @arrival_id.@vessel_details_id.@imbarcazione_id.nome")
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.aliasColumn('ship_rec','@sof_cargo_sof.ship_rec')
    
