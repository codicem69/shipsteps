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
        tbl.column('doc_onboard', dtype='DH', name_short='!![en]Documents onboard')
        tbl.column('remarks_rs', name_short='!![en]Receivers / Shippers Remarks')
        tbl.column('remarks_cte', name_short='!![en]Master Remarks')
        tbl.column('note', name_short='!![en]Note SOF')
        tbl.column('onbehalf', name_short='!![en]On behalf')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.aliasColumn('ship_rec','@sof_cargo_sof.ship_rec')
        tbl.aliasColumn('cargo_sof', '@sof_cargo_sof.@cargo_unl_load_id.cargo_sof',name_long='!![en]Cargo sof')
        tbl.aliasColumn('cargo_op', '@sof_cargo_sof.@cargo_unl_load_id.operation',name_long='!![en]Cago operation')

        tbl.formulaColumn('sof_det',"@arrival_id.reference_num || ' - ' || @arrival_id.date || ' - ' || @arrival_id.@vessel_details_id.@imbarcazione_id.nome")
        tbl.formulaColumn('nor_tend_txt', """CASE WHEN $nor_tend is not null THEN 'NOR tendered' ELSE '' END""", dtype='T')
        tbl.formulaColumn('nor_rec_txt', """CASE WHEN $nor_rec is not null THEN 'NOR received' ELSE '' END""", dtype='T')
        tbl.formulaColumn('nor_acc_txt', """CASE WHEN $nor_acc is not null THEN 'NOR acceppted' ELSE '' END""", dtype='T')
        tbl.formulaColumn('ops_commenced_txt', """CASE WHEN $ops_commenced is not null AND $cargo_op = 'U' THEN 'Unloading commenced ' 
                                                  WHEN $ops_commenced is not null AND $cargo_op = 'L' THEN 'Loading commenced ' ELSE '' END""", dtype='T')
        tbl.formulaColumn('ops_completed_txt', """CASE WHEN $ops_completed is not null AND $cargo_op = 'U' THEN 'Unloading completed ' 
                                                  WHEN $ops_completed is not null AND $cargo_op = 'L' THEN 'Loading completed ' ELSE '' END""", dtype='T')
        tbl.formulaColumn('doc_onboard_txt', """CASE WHEN $doc_onboard is not null THEN  :onboard END""",  dtype='T', var_onboard="cargo's documents on board")
        tbl.formulaColumn('note_txt', """CASE WHEN $note is not null THEN 'Notes' || '<br>'  ELSE '' END""", dtype='T')
        
        
        tbl.formulaColumn('time_sof', """coalesce('NOR tendered ' || to_char($nor_tend, :df), '') || '<br>' || coalesce('NOR received ' || to_char($nor_rec, :df),'') || '<br>' ||
                                         coalesce('NOR accepted ' || $nor_acc, '') || '<br>' || $ops_commenced_txt || to_char($ops_commenced, :df) || '<br>' || 
                                         $ops_completed_txt || to_char(ops_completed, :df) || '<br>' || coalesce(:onboard || to_char($doc_onboard,:df),'')""",var_onboard="Cargo's documents on board ",var_df='DD-MM-YYYY HH:MI')
    
